import hassapi as hass
import datetime

"""
clean_house is an app responsible of the scheduling of Spiroo
Functionality :
. Inform Edith of upcomming cleaning (30 minutes before)
. Starts Spiroo
. Handle cancelation of cleaning if requested by Edith
"""
class clean_house(hass.Hass):
  def initialize(self):
    runtime = datetime.time(16,0,0)
    self.run_daily(self.callback_pre_cleaning, runtime)
    self.listen_event(self.callback_cancel_cleaning , "DELAYED_AUTOMATION_CANCELED")
    self.log("House cleaning Automation initialized")

 
  """
  Callback triggered everyday at 16:00. A test will be made to check if 
    we are on a working day (binary_sensor.workday_today) 
    we are not, right now, in cleaning state
    the home is not occupied
    the last cleaning happend more than 36 hours ago
  Goals :
  . Schedule cleaning in 30 minutes
  . Inform Edith that Spiroo will start in 30 minutes
  """ 
  def callback_pre_cleaning(self, kwargs):
    if self.get_state("binary_sensor.workday_today") == "on" and self.get_state("vacuum.spiroo") != "cleaning" and self.get_state("binary_sensor.home_occupied") == "off": 
      last_cleaning = self.parse_datetime(self.get_state("vacuum.spiroo", attribute="clean_start"))
      now = self.datetime()
      diff = now - last_cleaning
      if diff > datetime.timedelta(hours = 36):
        self.log("House cleaning will start in 30 minutes. Sending event for potential cancel by Edith")
        delay = 1800
        # Schedule cleaning in 30 minutes via callback callback_cleaning
        self.cleaning_handle = self.run_in(self.callback_cleaning, delay)
        # Fire even DELAYED_AUTOMATION_NOTIFICATION with payload clean_house. See app "Notify" that will receive it
        self.fire_event("DELAYED_AUTOMATION_NOTIFICATION", payload = "clean_house")


  """
  Callback triggered 30 minutes after callback_pre_cleaning if not cancelled
  Goals : 
  . Start Spiroo
  """ 
  def callback_cleaning(self, kwargs):
    self.log("House cleaning will start now")
    # Start Spiroo
    self.call_service("neato/custom_cleaning" , entity_id = "vacuum.spiroo" , category = 4 , mode  = 1 , navigation = 1)


  """
  Callback triggered when the app receives an event DELAYED_AUTOMATION_CANCELED. Only payload clean_house supported in this app.
  See app "Notify" that will fire this event
  Goals : 
  . Cancel cleaning
  """     
  def callback_cancel_cleaning(self, event_name, data, kwargs):
    payload = data["payload"]
    if payload == "clean_house":
      self.log("House cleaning canceled")
      # Cancel cleaning
      self.cancel_timer(self.cleaning_handle)

