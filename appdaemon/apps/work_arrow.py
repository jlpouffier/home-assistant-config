import hassapi as hass
import datetime

class work_arrow(hass.Hass):
    def initialize(self):
        runtime = datetime.time(3,0,0)
        self.run_daily(self.callback_prepare_app, runtime)
        # Fallback if the app starts after 3am and before the wakeup time...
        if self.now_is_between("03:00:00" , self.get_state("input_datetime.wake_up_time")):
            self.run_in(self.callback_prepare_app, 0)
        self.log("Work Arrow Automation initialized")

    def callback_prepare_app(self, kwargs):
        self.last_arrival_datetime_green = datetime.datetime.combine(self.date() , datetime.time(8,0))
        self.last_arrival_datetime_orange = datetime.datetime.combine(self.date() , datetime.time(8,20))

        wake_up_time = self.parse_time(self.get_state("input_datetime.wake_up_time"))
        wake_up_datetime = datetime.datetime.combine(self.date() , wake_up_time)
        
        if wake_up_datetime > self.datetime() + datetime.timedelta(minutes = 1) and \
           self.get_state("binary_sensor.workday_today") == "on" and \
           wake_up_datetime < self.last_arrival_datetime_green and \
           self.last_arrival_datetime_green < self.last_arrival_datetime_orange:
            
            self.run_at(self.callback_start_app, wake_up_datetime)
            self.run_at(self.callback_stop_app, self.last_arrival_datetime_orange)
        
    def callback_start_app(self, kwargs):
        self.log("The work arrow automation is starting ...")
        self.current_urgency = self.compute_urgency()
        self.handle_led(self.current_urgency)
        self.handle = self.run_minutely(self.callback_refresh, datetime.time(0,0,30))
        
    def callback_stop_app(self, kwargs):
        self.log("The work arrow automation is stopping ...")
        self.cancel_timer(self.handle)
        self.handle_led(-1)

    def callback_refresh(self, kwargs):
        tmp_urgency = self.compute_urgency()
        
        if tmp_urgency != self.current_urgency:
            self.current_urgency = tmp_urgency
            self.handle_led(self.current_urgency)


    def handle_led(self, urgency):
        if urgency == 0:
            self.log("Urgency is minimal... Turning arrow accordingly (GREEN)...")
            self.call_service("light/turn_on" , entity_id = "light.wled_work_arrow", color_name = "green" , brightness_pct = 100, effect = "Solid")
        elif urgency == 1:
            self.log("Urgency is medium... Turning arrow accordingly (ORANGE)...")
            self.call_service("light/turn_on" , entity_id = "light.wled_work_arrow", color_name = "orange" , brightness_pct = 100, effect = "Breathe")
        elif urgency == 2:
            self.log("Urgency is critical... Turning arrow accordingly (RED)...")
            self.call_service("light/turn_on" , entity_id = "light.wled_work_arrow", color_name = "red" , brightness_pct = 100, effect = "Fade")
        elif urgency == -1:
            self.log ("Turning off Arrow")
            self.call_service("light/turn_off" , entity_id = "light.wled_work_arrow")

                      
    def compute_urgency(self):
        travel_duration_min = self.get_state("sensor.home_to_ricardo", attribute = "duration")
        predicted_arrival_datetime = self.datetime() + datetime.timedelta(minutes = travel_duration_min)
        
        if predicted_arrival_datetime <= self.last_arrival_datetime_green:
            return 0
        elif predicted_arrival_datetime <= self.last_arrival_datetime_orange:
            return 1
        else:
            return 2
            