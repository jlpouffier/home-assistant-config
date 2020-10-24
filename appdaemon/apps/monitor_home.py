import hassapi as hass


class monitor_home(hass.Hass): 
  def initialize(self):
    self.listen_state(self.callback_home_empty , "binary_sensor.home_occupied" , old = "on" , new = "off")
    
    self.log("Monitor Home initialized")

  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    # test if lights are still on
    if self.get_state("light.interior_lights") == "on":
      self.log("Detecting home empty and lights on. Notifying it...")
      self.fire_event("NOTIFY", payload = "lights_still_on")

    # test if TV is still on
    if self.get_state("media_player.philips_android_tv") not in ["off", "standby", "unavailable"]:
      self.log("Detecting home empty and TV on. Notifying it...")
      self.fire_event("NOTIFY", payload = "tv_still_on")

    # test if the climate control is still on
    if self.get_state("climate.salon") != "off":
      self.log("Detecting home empty and climate on. Notifying it...")
      self.fire_event("NOTIFY", payload = "climate_still_on")