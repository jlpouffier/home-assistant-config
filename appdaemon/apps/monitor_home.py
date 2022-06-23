import hassapi as hass

"""
monitor_home is an app responsible of the monitoring the home 

Functionalities :
. RTH Spirro if home becomes occupied
. Stop presence simulator if home becomes occupied

Notifications :
. Home empty and Lights on
. Home empty and TV on
. Home empty and coffee maker on

. Coffe maker on for more than 90 minutes

"""
class monitor_home(hass.Hass): 
  def initialize(self):
    self.listen_state(self.callback_home_empty , "binary_sensor.home_occupied" , old = "on" , new = "off")
    self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" , old = "off" , new = "on")
    self.listen_state(self.callback_coffee_maker_on_since_too_long , "switch.coffeemaker" , new = "on", duration = 5400)
    
    self.log("Monitor Home initialized")

  """
  Callback triggered when the home becomes not occupied
  Goals :
  . Send notification(s)
  """
  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    # test if lights are still on
    test = self.get_state("light.all_lights")
    self.log(test)
    if self.get_state("light.all_lights") == "on":
      self.log("Detecting home empty and lights on. Notifying it...")
      self.fire_event("NOTIFY", payload = "lights_still_on")

    # test if TV is still on
    if self.get_state("media_player.philips_android_tv") not in ["off", "standby", "unavailable"]:
      self.log("Detecting home empty and TV on. Notifying it...")
      self.fire_event("NOTIFY", payload = "tv_still_on")

    # test is coffe maker still on
    if self.get_state("switch.coffeemaker") == "on":
      self.log("Detecting home empty and coffee maker on. Notifying it...")
      self.fire_event("NOTIFY", payload = "coffee_maker_still_on")


  """
  Callback triggered when the home becomes occupied
  Goals :
  . Stop presence simulator (If turned on)
  . Stop Spiroo (if spirroo  on) 
  """
  def callback_home_occupied(self, entity, attribute, old, new, kwargs):
    self.log("Detecting home occupied...")
    if self.get_state("input_boolean.presence_simulator_switch") == "on":
      # Stopping Dog Mode
      self.log("Stopping Presence Simulator")
      self.call_service("input_boolean/toggle", entity_id = "input_boolean.presence_simulator_switch")

    if self.get_state("vacuum.spiroo") == 'cleaning':
      # Stopping Spiroo
      self.log("RTH Spirro") 
      self.call_service("vacuum/return_to_base" , entity_id = "vacuum.spiroo")

  """
  Callback triggered when coffee maker on for more than 90 minutes
  Goals :
  . Send notification(s)
  """
  def callback_coffee_maker_on_since_too_long(self, entity, attribute, old, new, kwargs):
    self.log("Detecting coffee maker on for more than 90 minutes. Notifying it...")
    self.fire_event("NOTIFY", payload = "coffee_maker_on_since_too_long")