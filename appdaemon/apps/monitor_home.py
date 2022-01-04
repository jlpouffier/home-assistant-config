import hassapi as hass

"""
monitor_home is an app responsible of the monitoring the home 

Functionalities :
. Turn on and off Google Home based on home occupancy (If Dog Mode is off)

Notifications :
. Home empty and Lights on (If Dog Mode is off)
. Home empty and TV on
. Home empty and climate on
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
  . Turn off Google home (If Dog mode if off)
  . Send notification(s)
  """
  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    # If Dog Mode is off ...
    if self.get_state("input_boolean.dog_mode") == "off":

      # home empty >> stopping google home
      self.log("Detecting home empty... Stopping Google Home")
      self.call_service("switch/turn_off" , entity_id = "switch.google_home")

      # test if lights are still on
      if self.get_state("light.interior_lights") == "on":
        self.log("Detecting home empty and lights on. Notifying it...")
        self.fire_event("NOTIFY", payload = "lights_still_on")

    # test if TV is still on
    if self.get_state("media_player.philips_android_tv") not in ["off", "standby", "unavailable"]:
      self.log("Detecting home empty and TV on. Notifying it...")
      self.fire_event("NOTIFY", payload = "tv_still_on")

    # test if the climate control is still on
    if self.get_state("climate.salon") != "off" or self.get_state("climate.chambre") != "off" or self.get_state("climate.bureau") != "off":
      self.log("Detecting home empty and climate on. Notifying it...")
      self.fire_event("NOTIFY", payload = "climate_still_on")

    # test is coffe maker still on
    if self.get_state("switch.coffeemaker") == "on":
      self.log("Detecting home empty and coffee maker on. Notifying it...")
      self.fire_event("NOTIFY", payload = "coffee_maker_still_on")


  """
  Callback triggered when the home becomes occupied
  Goals :
  . Turn on Google home (If turned of)
  . Stop Dog mode (If turned on)
  """
  def callback_home_occupied(self, entity, attribute, old, new, kwargs):
    if self.get_state("switch.google_home") == "off":
      # home occupied >> starting google home
      self.log("Detecting home occupied... Starting Google Home")
      self.call_service("switch/turn_on" , entity_id = "switch.google_home")

    if self.get_state("input_boolean.dog_mode") == "on":
      # Stopping Dog Mode
      self.call_service("input_boolean/toggle", entity_id = "input_boolean.dog_mode")

  """
  Callback triggered when coffee maker on for more than 90 minutes
  Goals :
  . Send notification(s)
  """
  def callback_coffee_maker_on_since_too_long(self, entity, attribute, old, new, kwargs):
    self.log("Detecting coffee maker on for more than 90 minutes. Notifying it...")
    self.fire_event("NOTIFY", payload = "coffee_maker_on_since_too_long")