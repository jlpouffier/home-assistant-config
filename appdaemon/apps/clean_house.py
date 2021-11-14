import hassapi as hass
import datetime

"""
clean_house is an app responsible of the scheduling of Spiroo

Functionalities :
. Starts Spiroo when needed
. Handle cancelation of cleaning if requested

Notifications :
. Cleaning Scheduled
. Cleaning Started
. Cleaning Finished
. Spiroo error
. Spiroo noton the dock
"""
class clean_house(hass.Hass):
  def initialize(self):
    runtime = datetime.time(16,0,0)
    self.listen_state(self.callback_home_empty_for_more_than_30_minutes, "binary_sensor.home_occupied", old = "on", new = "off", duration = 1800)
    self.listen_event(self.callback_cancel_cleaning , "CANCEL_AUTOMATION", payload = "clean_house")
    self.listen_state(self.callback_spiroo_started, "vacuum.spiroo" , old = "docked" , new = "cleaning")
    self.listen_state(self.callback_spiroo_cleaning_for_more_than_15_minutes, "vacuum.spiroo" , new = "cleaning", duration = 900)
    self.listen_state(self.callback_spiroo_finished, "vacuum.spiroo" , old = "paused" , new = "docked")
    self.listen_state(self.callback_spiroo_finished, "vacuum.spiroo" , old = "cleaning" , new = "docked")
    self.listen_state(self.callback_spiroo_finished, "vacuum.spiroo" , old = "returning" , new = "docked")
    self.listen_state(self.callback_spiroo_error, "vacuum.spiroo" , new = "error")
    self.listen_state(self.callback_spiroo_idle, "vacuum.spiroo" , new = "idle" , duration = 1800)

    self.log("House cleaning Automation initialized")

  """
  Callback triggered when the home is empty for more than 30 minutes
  Goals :
  . Check if the alst clean-up was done more then 36 hours ago
  . Check if dog mode is off
  . Check if we are not cleaning right now
  . If all 3 conditions are met:
    . Schedule cleaning in 30 minutes 
    . Send a notification
  """ 
  def callback_home_empty_for_more_than_30_minutes(self, entity, attribute, old, new, kwargs):
    self.log("Home empty for more than 30 minutes, checking if Spiroo should clean the home now ... ")
    # Home concidered Dirty if last clean-up was done more then 36 hours ago
    now = self.datetime(True)
    last_cleaning = self.parse_datetime(self.get_state("input_datetime.dernier_nettoyage_de_spiroo"), aware = True) 
    diff = now - last_cleaning
    is_home_dirty = True if diff > datetime.timedelta(hours = 36) else False

    # Getting Dog mode status
    is_dog_mode = True if self.get_state("input_boolean.dog_mode") == "on" else False

    # Are we cleaning right now ?
    is_cleaning_right_now = True if self.get_state("vacuum.spiroo") == "cleaning" else False

    if is_home_dirty and not is_dog_mode and not is_cleaning_right_now:
      self.log("House cleaning will start in 30 minutes. Sending event for potential cancel by Notify")
      delay = 1800
      # Schedule cleaning in 30 minutes via callback callback_cleaning
      self.cleaning_handle = self.run_in(self.callback_cleaning, delay)
      # Fire even NOTIFY with payload cleaning_scheduled. See app "Notify" that will receive it
      self.fire_event("NOTIFY", payload = "cleaning_scheduled")


  """
  Callback triggered 30 minutes after callback_home_empty_for_more_than_30_minutes if not cancelled
  Goals : 
  . Start Spiroo
  """ 
  def callback_cleaning(self, kwargs):
    self.log("House cleaning will start now")
    # Start Spiroo
    self.call_service("vacuum/start" , entity_id = "vacuum.spiroo")


  """
  Callback triggered when the app receives an event CANCEL_AUTOMATION with payload "clean_house"
  See app "Notify" that will fire this event
  Goals : 
  . Cancel cleaning
  """     
  def callback_cancel_cleaning(self, event_name, data, kwargs):
    self.log("House cleaning canceled")
    # Cancel cleaning
    self.cancel_timer(self.cleaning_handle)


  """
  Callback triggered when Spiroo is starting
  Goals : 
  . Send a notification
  """   
  def callback_spiroo_started(self, entity, attribute, old, new, kwargs):
    self.log("Detecting that Spiroo is starting. Notifying it...")
    self.fire_event("NOTIFY", payload = "cleaning_started")

  """
  Callback triggered when 
  Goals : 
  . 
  """   
  def callback_spiroo_cleaning_for_more_than_15_minutes(self, entity, attribute, old, new, kwargs):
    self.log("Spiroo is cleaning since more than 15 minutes, updating the last clean-up datetime...")
    self.call_service("input_datetime/set_datetime", entity_id = "input_datetime.dernier_nettoyage_de_spiroo", datetime = self.datetime(True))

  """
  Callback triggered when Spiroo is finished
  Goals : 
  . Send a notification
  """ 
  def callback_spiroo_finished(self, entity, attribute, old, new, kwargs):
    self.log("Detecting that Spiroo has finished. Notifying it...")
    self.fire_event("NOTIFY", payload = "cleaning_finished")

  """
  Callback triggered when Spiroo is in error
  Goals : 
  . Send a notification
  """ 
  def callback_spiroo_error(self, entity, attribute, old, new, kwargs):
    if old != new:
      self.log("Detecting that Spiroo is in trouble. Notifying it...")
      self.fire_event("NOTIFY", payload = "cleaning_error")

  """
  Callback triggered when is not on the dock since more than 30 mintues
  Goals : 
  . Send a notification
  """ 
  def callback_spiroo_idle(self, entity, attribute, old, new, kwargs):
    if old != new:
      self.log("Detecting that Spiroo is not plugged since more than 30 miuntes. Notifying it...")
      self.fire_event("NOTIFY", payload = "cleaning_idle")


