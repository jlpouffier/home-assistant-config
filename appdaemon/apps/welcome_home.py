import hassapi as hass

"""
welcome_home is an app responsible of turning on lights when we arrive at home
Functionality :
. Activate only if the home is not occupied at sun-set
. Run the welcome routine only once
. Handle edge case when the home stays un-occupied for the whole night
"""
class welcome_home(hass.Hass):
  def initialize(self):
    # Run every day at sunset the preparation of the welcome home automation
    self.run_at_sunset(self.callback_prepare_welcome_home)
    self.log("Welcome Home Automation initialized")

  """
  Callback trigerred every day at sunset
  Goals
  . Check if the home is occupied, and if not : Register callbacks to welcome humans home
  """
  def callback_prepare_welcome_home(self, kwargs):
    # At sunset , if the home is not occupied ....
    if self.get_state("binary_sensor.home_occupied") == "off":
      self.log("The sun as set & the home is not occupied : Registering welcome home automation")
      # Register a callback for the welcome home automation (one shot)
      self.callback_welcome_home_handle = self.listen_state(self.callback_welcome_home, "binary_sensor.home_occupied", old = "off", new = "on", oneshot = True)
      # Register a callback to cancel the welcome home automation
      self.callback_cancel_welcome_home_handle = self.run_once(self.callback_cancel_welcome_home, "sunrise")

  """
  Callback trigerred ONCE if the home becomes occupied 
  Goals
  . Lights sequence
  """
  def callback_welcome_home(self, entity, attribute, old, new, kwargs):
    # When presence is detected ....
    sequence = [
      {"sleep": 1},
      {"hue/activate_scene": {
        "entity_id": "scene.entree_entree_100",
        "transition": 3}},
      {"sleep": 2},
      {"hue/activate_scene": {
        "entity_id": "scene.salon_salon_100",
        "transition": 3}},
      {"sleep": 2},
      {"hue/activate_scene": {
        "entity_id": "scene.cuisine_cuisine_100",
        "transition": 3}}
    ]
    self.log("Welcome home : turning on lights. (This automation won't be run until tomorrow 4pm the soonest)")
    # ... Turn lights on ...
    self.run_sequence(sequence)
    # ... abort the cancel
    self.cancel_timer(self.callback_cancel_welcome_home_handle)

  """
  Callback trigerred if no-one came home at sunrise the next day.
  Goals
  . Cancel the welcome home callback.
  """
  def callback_cancel_welcome_home(self, kwargs):
    # If no-one came home during the night ...
    self.log("Nobody came home this night ... Canceling the welcome home automation")
    # Abort the welcome home automoation
    self.cancel_listen_state(self.callback_welcome_home_handle) 

