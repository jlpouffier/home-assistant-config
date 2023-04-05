import hassapi as hass
import datetime

"""
wake_up is an app responsible of the "wake-up experience" of the home
Functionality : 
. Register the wake up time every day at 3 am based on user input time 
. Only turn on if it's a work day (Week-end and French holidays supported)
. Progressively turn on lights before and after alarm
. Turn on the coffee maker 30 minutes before waking up
Notifications :
. Alarm time hanged on JL phone  > Change wake-up time possible 

"""
class wake_up(hass.Hass):
  def initialize(self):
    # Run every day at 3 am the preparation of the wake-up
    runtime = datetime.time(3,0,0)
    self.run_daily(self.callback_schedule_wake_up, runtime)
    self.listen_state(self.callback_jl_phone_alarm_changed, "sensor.pixel_6_next_alarm")
    self.listen_event(self.callback_button_clicked_set_new_wake_up_time, "mobile_app_notification_action", action = "set_new_wake_up_time")

    # Fallback if the app starts after 3am and before the wakeup time...
    if self.now_is_between("03:00:00" , self.get_state("input_datetime.wake_up_time")):
      self.run_in(self.callback_schedule_wake_up, 0)



  """
  Callback trigerred every dat at 3am
  Goals
  . Check if we are on a work day
  . Compute the wake-up time based on an home assistant input
  . Register callbacks to turn on wake-up
  """
  def callback_schedule_wake_up(self, kwargs):
    # If it' s a workday and home is actually occupied ...
    if self.get_state("binary_sensor.workday_today") == "on" and self.get_state("binary_sensor.home_occupied") == "on":
      # Fetch wake time from input_datetime.wake_up_time ...
      input_time = self.parse_time(self.get_state("input_datetime.wake_up_time"))
      today_date = self.date()
      # Wake up time is input time - 5 minutes
      wake_up_datetime = datetime.datetime.combine(today_date , input_time)  - datetime.timedelta(minutes = 5) 
      # Coffee maker turn on time is input time - 30 minutes
      coffee_maker_turn_on_time = datetime.datetime.combine(today_date , input_time)  - datetime.timedelta(minutes = 30) 

      # Only register callbacks if the wake-up time is in the future (Strict future ! so I have added 1 minute)
      if wake_up_datetime > self.datetime() + datetime.timedelta(minutes = 1) :
          self.log("Wake up automation will be turned on at :")
          self.log(wake_up_datetime)
          # ... and register the wake-up callback
          self.run_at(self.callback_wake_up, wake_up_datetime)
      else: 
          self.log("Wake up automation won't be turned on today because wake-up time is in the past")
          self.log(wake_up_datetime)

      # Only register callbacks if the Coffee maker turn on time is in the future (Strict future ! so I have added 1 minute)
      if coffee_maker_turn_on_time > self.datetime() + datetime.timedelta(minutes = 1) and self.args["turn_on_coffee_maker"] :
          self.log("Coffee maker will be turned on at :")
          self.log(coffee_maker_turn_on_time)
          # ... and register the wake-up callback
          self.run_at(self.callback_turn_on_coffee_maker, coffee_maker_turn_on_time)
      else:
          self.log("Coffee maker won't be turned on today because <coffee maker turn on> time is in the past :")
          self.log(coffee_maker_turn_on_time)

  '''
  Callback trigerred 5 minutes before wake-up time
  Goals
  . Light sequence (if home occupied)
  '''
  def callback_wake_up(self, kwargs):
    '''
    Light sequence (with a wake up time at 6:40)

    6:35
    Make sure the lights are off on the bedroom
    Turn on the bloom to 100% in 5 minutes

    6:40
    Turn on the Ceiling lights to 100% in 5 minutes

    6:50
    Turn on the fairy lights
    '''
    sequence = [
      {"light/turn_off": {
        "entity_id": "light.chambre"}},
      {"light/turn_on": {
        "entity_id": "light.chambre_bloom",
        "transition": 300,
        "brightness_pct": 100,
        "rgb_color":[255,159,1] }},
      {"sleep": 300},
      {"light/turn_on": {
        "entity_id": "light.chambre_suspension",
        "transition": 300,
        "brightness_pct": 100 }},
      {"light/turn_on": {
        "entity_id": "light.chambre_chevet_jl",
        "transition": 300,
        "brightness_pct": 100 }},
      {"light/turn_on": {
        "entity_id": "light.chambre_chevet_valentine",
        "transition": 300,
        "brightness_pct": 100 }},  
      {"sleep": 600},
      {"light/turn_on": {
        "entity_id": "light.chambre_guirlande"}}
    ]

    self.log("Wake up automation !")
    self.run_sequence(sequence)

  '''
  Callback trigerred 30 minutes before wake-up time
  Goals
  . Turn-on coffee maker (Pre-heating)
  '''
  def callback_turn_on_coffee_maker(self, kwargs):
    self.log("Turning on coffee maker !")
    self.call_service("switch/turn_on" , entity_id = "switch.coffeemaker")

  '''
  Callback trigerred when JL's alarm changes
  Goals
  . Send notification
  '''
  def callback_jl_phone_alarm_changed(self, entity, attribute, old, new, kwargs):
    if new != "unavailable":
      jl_home_alarm_time = (self.convert_utc(new) + datetime.timedelta(minutes = self.get_tz_offset())).time()
      current_wake_up_time = self.parse_time(self.get_state("input_datetime.wake_up_time"))
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