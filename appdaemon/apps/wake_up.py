import hassapi as hass
import datetime

"""
wake_up is an app responsible of the "wake-up experience" of the home
Functionality : 
. Only turn on if it's a work day (Week-end and French holidays supported)
. Progressively turn on lights before and after alarm
. Turn on the coffee maker 30 minutes before waking up
Notifications :
. Alarm time hanged on JL phone  > Change wake-up time possible 
"""
class wake_up(hass.Hass):
  def initialize(self):
    self.light_timer_handle = None
    self.coffee_maker_handle = None

    self.listen_state(self.callback_wake_up_time_changed, "input_datetime.wake_up_time", immediate = True)
    self.listen_state(self.callback_wake_up_time_lights_changed, "input_datetime.wake_up_time_lights", immediate = True)
    self.listen_state(self.callback_wake_up_time_coffee_maker_changed, "input_datetime.wake_up_time_coffee_maker", immediate = True)

    self.listen_state(self.callback_jl_phone_alarm_changed, "sensor.pixel_6_next_alarm")
    self.listen_event(self.callback_button_clicked_set_new_wake_up_time, "mobile_app_notification_action", action = "set_new_wake_up_time")

  '''
  Callback trigerred when wake-up time changed
  Goals
  . change light and coffee maker schedule
  '''
  def callback_wake_up_time_changed(self, entity, attribute, old, new, kwargs):
    self.log("Wake-up time changed... Computing light and coffee maker schedules...")
    wake_up_time_lights = datetime.datetime.combine(self.date() ,  self.parse_time(self.entities.input_datetime.wake_up_time.state)) - datetime.timedelta(minutes = 5)
    wake_up_time_coffee_maker = datetime.datetime.combine(self.date() ,  self.parse_time(self.entities.input_datetime.wake_up_time.state)) - datetime.timedelta(minutes = 30)
    self.call_service("input_datetime/set_datetime", entity_id = "input_datetime.wake_up_time_lights", time = wake_up_time_lights.strftime("%H:%M:%S"))
    self.call_service("input_datetime/set_datetime", entity_id = "input_datetime.wake_up_time_coffee_maker", time = wake_up_time_coffee_maker.strftime("%H:%M:%S"))

  '''
  Callback trigerred when light schedule changed
  Goals
  . Deregister old timer, register new timer
  '''
  def callback_wake_up_time_lights_changed(self, entity, attribute, old, new, kwargs):
    self.log("Light schedule changed... Changing scheduler ...")
    if self.light_timer_handle != None:
      self.cancel_timer(self.light_timer_handle)
    self.light_timer_handle = self.run_daily(self.callback_turn_on_lights, new)
  
  '''
  Callback trigerred when coffee maker schedule changed
  Goals
  . Deregister old timer, register new timer
  '''
  def callback_wake_up_time_coffee_maker_changed(self, entity, attribute, old, new, kwargs):
    self.log("Coffee Maker schedule changed... Changing scheduler ...")
    if self.coffee_maker_handle != None:
      self.cancel_timer(self.coffee_maker_handle)
    self.coffee_maker_handle = self.run_daily(self.callback_turn_on_coffee_maker, new)

  '''
  Callback trigerred at light time (5 minutes before wake-up time)
  Goals
  . Light sequence (if home occupied and workday)
  '''
  def callback_turn_on_lights(self, kwargs):
    if self.entities.binary_sensor.workday_today.state == "on" and self.entities.binary_sensor.home_occupied.state == "on":
      self.log("Turning on lights")
      self.call_service("script/wake_up")

  '''
  Callback trigerred at coffee maker time (30 minutes before wake-up time)
  Goals
  . Turn-on coffee maker (if home occupied and workday)
  '''
  def callback_turn_on_coffee_maker(self, kwargs):
    if self.entities.binary_sensor.workday_today.state == "on" and self.entities.binary_sensor.home_occupied.state == "on" and self.entities.input_boolean.wake_up_automation_control_coffee_maker.state == "on":
      self.log("Turning on coffee maker")
      self.call_service("switch/turn_on" , entity_id = "switch.coffeemaker")

  '''
  Callback trigerred when JL's alarm changes
  Goals
  . Send notification
  '''
  def callback_jl_phone_alarm_changed(self, entity, attribute, old, new, kwargs):
    if new != "unavailable":
      jl_home_alarm_time = (self.convert_utc(new) + datetime.timedelta(minutes = self.get_tz_offset())).time()
      current_wake_up_time = self.parse_time(self.entities.input_datetime.wake_up_time.state)
      if jl_home_alarm_time != current_wake_up_time:
        # Current Wake-up time and Phone Alarm time are different : Notifying it
        self.log("Phone alarmed different than Wake-up time. Notifying it ...")
        self.fire_event("NOTIFIER",
          action = "send_to_jl",
          title = "⏰ Alarme réglée pour " +  str(jl_home_alarm_time), 
          message = "Utiliser pour le réveil inteligent ?",
          callback = [{
            "title" : "Oui",
            "event" : "set_new_wake_up_time"}],
          click_url="/lovelace/night",
          icon = "mdi:alarm",
          tag = "jl_phone_alarm_changed")

  """
  Callback triggered when button "set_new_wake_up_time" is clicked from a notification
  Goals :
  . Change the time of the wake-up automations (input_datetime.wake_up_time)
  """
  def callback_button_clicked_set_new_wake_up_time(self, event_name, data, kwargs):
    new_time = self.get_state('sensor.pixel_6_next_alarm')
    new_time = (self.convert_utc(new_time) + datetime.timedelta(minutes = self.get_tz_offset())).time()
    self.log("Notification button clicked : Setting wake_up_time to JL's phone alarm time ... ") 
    self.call_service("input_datetime/set_datetime", entity_id = 'input_datetime.wake_up_time', time = new_time)