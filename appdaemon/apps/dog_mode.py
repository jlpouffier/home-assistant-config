import hassapi as hass

"""
dog_mode is an app responsible of keeping my dog entertained when I am not at home

Functionalities :
. Turn on and off "Dog Mode"
  . Dim lights 
  . Play music

Notifications :
. None

"""
class dog_mode(hass.Hass): 
  def initialize(self):
    self.listen_state(self.callback_dog_mode_on , "input_boolean.dog_mode" , old = "off" , new = "on")
    self.listen_state(self.callback_dog_mode_off , "input_boolean.dog_mode" , old = "on" , new = "off")

    self.log("Dog Mode initialized")

  """
  Callback triggered when Dog Mode is activated
  Goals :
  . Turn off all lights
  . Turn on living room and Kitchen at 1% (If the sun us down)
  . Register callbacks to turn on/off lights based on the sun
  . Play the "Dog mode" playlist on Spotify
  """     
  def callback_dog_mode_on(self, entity, attribute, old, new, kwargs):
    # Turn off all lights
    self.call_service("script/1619802584518")

    sequence = []

    # Turn on living room and Kitchen at 1% (If the sun us down)
    if self.get_state("sun.sun") == "below_horizon":
      sequence.extend([
        {"light/turn_on": {
          "entity_id": "light.cuisine",
          "brightness_pct": 1}},
        {"light/turn_on": {
          "entity_id": "light.salon",
          "brightness_pct": 1}}])

    # Play the "Dog mode" playlist on Spotify
    sequence.extend([
      {"spotcast/start": {
        "entity_id": "media_player.nest_mini_cuisine",
        "uri": "spotify:playlist:5eR0Js0wFpA9X9hkGMv7uq",
        "shuffle" : True,
        "random_song" : True,
        "start_volume" : 35}}])
    

    self.log("Turning on dog mode ...")
    self.run_sequence(sequence)

    # Register callbacks to turn on/off lights based on the sun
    self.sunset_handle = self.listen_state(self.callback_sunset, "sun.sun", new = "below_horizon")
    self.sunrise_handle = self.listen_state(self.callback_sunrise,  "sun.sun", new = "above_horizon")


  """
  Callback triggered when Dog Mode is deactivated
  Goals :
  . Stop playback
  . Turn on lights (if sun is down)
  . Turn off lights (if sun is up)
  """  
  def callback_dog_mode_off(self, entity, attribute, old, new, kwargs):
    self.log("Turning off dog mode ...")

    # Deregister callbacks
    self.cancel_listen_state(self.sunset_handle)
    self.cancel_listen_state(self.sunrise_handle)

    # Stop playback
    self.call_service("media_player/media_stop", entity_id = "media_player.nest_mini_cuisine")

    # Turn on lights (if sun is down)
    if self.get_state("sun.sun") == "below_horizon":
      self.call_service("script/lights_set_livingroom_kitchen_regular")

    # Turn off lights (if sun is up)
    else: 
      self.call_service("light/turn_off" , entity_id = "light.cuisine")
      self.call_service("light/turn_off" , entity_id = "light.salon")


  """
  Callback triggered when the sun is setting and the dog is at home
  Goals :
  . Turn on lights 
  """  
  def callback_sunset(self, entity, attribute, old, new, kwargs):
    if self.get_state("light.cuisine") != "on" or self.get_state("light.salon") != "on":
      sequence = [
        {"light/turn_on": {
          "entity_id": "light.cuisine",
          "brightness_pct": 1}},
        {"light/turn_on": {
          "entity_id": "light.salon",
          "brightness_pct": 1}}]

      self.log("Dog at home + Sun is down : Turning lights on ...")
      self.run_sequence(sequence)


  """
  Callback triggered when the sun is raising and the dog is at home
  Goals :
  . Turn off lights 
  """  
  def callback_sunrise(self, entity, attribute, old, new, kwargs):
    if self.get_state("light.cuisine") == "on" or self.get_state("light.salon") == "on":
      
      self.log("Dog is on house, sun is up : Turning lights off ...")
      self.call_service("light/turn_off" , entity_id = "light.cuisine")
      self.call_service("light/turn_off" , entity_id = "light.salon")


