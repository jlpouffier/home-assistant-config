import hassapi as hass

"""
watch_tv is an app responsible of the TV watching experience

Functionalities :
. Turn on and off Speaker based on TV state
. Turn on and off light when watching a movie
. Turn on and off light when playing the PS5

Notifications :
. None
"""
class watch_tv(hass.Hass):
  def initialize(self):

    # Listener to turn on or off the speakers based on the TV state.
    self.listen_state(self.callback_tv_on, "binary_sensor.is_tv_on", new = "on")
    self.listen_state(self.callback_tv_off, "binary_sensor.is_tv_on", new = "off")

    # The Light-TV automations will only run if the sun is down.  
    self.listen_state(self.callback_initialize_automations, "sun.sun", new = "below_horizon", immediate = True)
    self.listen_state(self.callback_stop_automations, "sun.sun", new = "above_horizon", immediate = True)

    # handles to register / unregister TV state change callbacks
    self.state_handles = []

    # Variable to store the old app to detect app changes. Initialized to the Android Home page
    self.old_app = "Android TV Launcher"

    # log
    self.log("Initialized")

  """
  Callback triggered when the TV is on
  Goals :
  . Start KEF LSX (and change source) if not turned on yet
  """ 
  def callback_tv_on(self, entity, attribute, old, new, kwargs):
    if self.get_state("media_player.kef") == "off" and self.get_state("script.turn_on_media_center") == "off":
      self.call_service("script/turn_on_media_center")

  """
  Callback triggered when the TV is off
  Goals :
  . Stop KEF LSX if still on
  """ 
  def callback_tv_off(self, entity, attribute, old, new, kwargs):
    if self.get_state("media_player.kef") == "on"  and self.get_state("script.turn_off_media_center") == "off":
      self.call_service("script/turn_off_media_center")
  
  """
  Callback triggered when the sun is below horizon
  Goals :
  . Start listing to TV state changes
  """ 
  def callback_initialize_automations(self, entity, attribute, old, new, kwargs):
    # Register TV state change callbacks 
    callback_tv_state_change_handle = self.listen_state(self.callback_tv_state_change, self.args["media_player_id"], immediate = True)
    callback_ps5_state_change_handle = self.listen_state(self.callback_ps5_state_change, "binary_sensor.is_ps5_used", immediate = True)

    # Store handles to deregister later.
    self.state_handles.append(callback_tv_state_change_handle)
    self.state_handles.append(callback_ps5_state_change_handle)

    self.log("Watch TV Automations starting ...")

  """
  Callback triggered when the sun is above horizon
  Goals :
  . Stop listening to TV state changes 
  """
  def callback_stop_automations(self, entity, attribute, old, new, kwargs):
    # Deregister TV state change callbacks
    while len(self.state_handles) >=1:
      handle = self.state_handles.pop()
      self.cancel_listen_state(handle)

    self.log("Watch TV Automations stopping for now ...")

  """
  Callback triggered when TV state changes
  Goals :
  . Turn on and off lights depending the on the TV state and the current app used 
  """
  def callback_tv_state_change(self, entity, attribute, old, new, kwargs):
    # Fetch the current app
    current_app = self.get_state(entity, attribute = "app_name")
    if current_app is None:
      current_app = "Android TV Launcher"

    # Log state change
    self.log_state_change(old, self.old_app, new, current_app)

    if old in ["off", "standby", "unavailable" , "paused", "unknown", "idle", None] and new == "playing":
      if self.is_app_controling_lights(current_app):
        #CALL SCRIPT
        self.log("TV playing : Lights dimmed")
        self.call_service("script/lights_set_tv")  
    
    elif old in ["playing" , None] and new == "paused":
      if self.is_app_controling_lights(current_app):
        #CALL SCRIPT
        self.log("TV paused : Lights partially un-dimmed")
        self.call_service("script/lights_set_tv_paused")        

    elif old in ["playing" , "paused"] and new in ["standby" , "off" , "unavailable", "unknown", "idle"]:
      if self.is_app_controling_lights(self.old_app):
        #CALL SCRIPT
        self.log("TV stopped : Lights fully un-dimmed")
        self.call_service("script/reset_lights_day_area")
      
    self.old_app = current_app

  """
  Callback triggered when the PS5 state change
  Goals :
  . Turn on and off lights based on PS5 state
  """
  def callback_ps5_state_change(self, entity, attribute, old, new, kwargs):
    if old in ["off" , None] and new == 'on':
        self.log("PS5 is use : Lights dimmed")
        self.call_service("script/lights_set_tv") 
    elif old == "on" and new == 'off':
        self.log("PS5 stopped : Lights fully un-dimmed")
        self.call_service("script/reset_lights_day_area")

  """
  Helper method:
  Does : 
  . nothing
  Returns : true if an app is controlling the light, false otherwise
  """
  def is_app_controling_lights(self, tv_app):
    if tv_app in self.args["supported_apps"]:
      return True
    else:
      return False

  """
  Helper method:
  Does : 
  . logs a human-reedable TV state change 
  Returns : nothing
  """
  def log_state_change(self, old, old_app, new, new_app):
    self.log("State changed: " + str(old) + " @ " + old_app + " > " + str(new) + " @ " + new_app)

