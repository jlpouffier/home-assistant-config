import hassapi as hass
import datetime

"""
wake_up is an app responsible of turning on lights at wake time
Functionality :
. Register the wake up time every day at 3 am based on user input time 
. Only turn on if it' s a work day
"""
class wake_up(hass.Hass):
  def initialize(self):
    # Run every day at 3 am the preparation of the wake-up
    runtime = datetime.time(3,0,0)
    self.run_daily(self.callback_schedule_wake_up, runtime)
    
    # Fallback if the app starts after 3am and before the wakeup time...
    if self.now_is_between("03:00:00" , self.get_state("input_datetime.wake_up_time")):
      self.run_in(self.callback_schedule_wake_up, 0)
      
    self.log("Waking-up Automations initialized")


  def callback_schedule_wake_up(self, kwargs):
    # If it' s a workday ...
    if self.get_state("binary_sensor.workday_today") == "on":
      # Fetch wake time from input_datetime.wake_up_time ...
      input_time = self.parse_time(self.get_state("input_datetime.wake_up_time"))
      today_date = self.date()
      # Wake up time is input time - 5 minutes
      wake_up_datetime = datetime.datetime.combine(today_date , input_time)  - datetime.timedelta(minutes = 5) 
      
      # Only register callbacks if the wake-up time is in the future (Strict future ! so I have added 1 minute)
      if wake_up_datetime > self.datetime() + datetime.timedelta(minutes = 1) :
          self.log("Wake up automation will be turned on at :")
          self.log(wake_up_datetime)
          # ... and register the wake-up callback
          self.run_at(self.callback_wake_up, wake_up_datetime)
      else: 
          self.log("Wake up automation won't be turned on today because wake-up time is in the past :")
          self.log(wake_up_datetime)

  '''
  With a wake up time at 6:50:

  6:45
  Make sure the lights are off on the bedroom
  Turn on the bloom to 100% in 5 minutes
  Wait 5 minutes

  6:50
  Turn on the Ceiling lights 1to 100% in 5 minutes
  Wait 10 minutes

  7:00
  Turn on the fairy lights
  Open the cover
  '''
  def callback_wake_up(self, kwargs):
    sequence = [
        {"light/turn_off": {
          "entity_id": "light.chambre_principale"}},
        {"light/turn_on": {
          "entity_id": "light.main_bedroom_bloom",
          "transition": 300,
          "brightness_pct": 100,
          "rgb_color":[255,159,1] }},
        {"sleep": 300},
        {"light/turn_on": {
          "entity_id": "light.main_bedroom_ceiling",
          "transition": 300,
          "brightness_pct": 100 }},
        {"sleep": 600},
        {"light/turn_on": {
          "entity_id": "light.main_bedroom_fairy_lights"}},
        {"cover/open_cover": {
          "entity_id": "cover.main_bedroom_roller_shutter"}},
      ]

    self.log("Wake up automation !")
    self.run_sequence(sequence)

