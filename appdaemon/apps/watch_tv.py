import hassapi as hass

"""


"""
class watch_tv(hass.Hass):
  def initialize(self):
    # The TV automations will only run if the sun is down.  
    self.listen_state(self.callback_initialize_automations, "sun.sun", new = "below_horizon", immediate = True)
    self.listen_state(self.callback_stop_automations, "sun.sun", new = "above_horizon", immediate = True)

    # handles to register / unregister TV state change callbacks
    self.state_handles = []

    # Variable to store the old app to detect app changes. Initialized to the Android Home page
    self.old_app = "com.google.android.tvlauncher"

    self.log("Watch TV Automations initialized")
 
  """


  """
  def callback_initialize_automations(self, entity, attribute, old, new, kwargs):
    # Register TV state change callbacks 
    callback_tv_state_change_handle = self.listen_state(self.callback_tv_state_change, "media_player.philips_android_tv", immediate = True)
    callback_ps5_state_change_handle = self.listen_state(self.callback_ps5_state_change, "binary_sensor.is_ps5_used", immediate = True)

    # Store handles to deregister later.
    self.state_handles.append(callback_tv_state_change_handle)
    self.state_handles.append(callback_ps5_state_change_handle)

    self.log("Watch TV Automations starting now ...")

  """


  """
  def callback_stop_automations(self, entity, attribute, old, new, kwargs):
    # Deregister TV state change callbacks
    for handle in self.state_handles:
      self.cancel_listen_state(handle)

    self.log("Watch TV Automations stopping for now ...")

  """


  """
  def callback_tv_state_change(self, entity, attribute, old, new, kwargs):
    # Get attributes of the TV and fetch the current app
    tv_attributes = self.get_state(entity, attribute = "all")
    if 'attributes' in tv_attributes and 'app_id' in tv_attributes["attributes"]:
      current_app = tv_attributes["attributes"]["app_id"] 
    else:
      current_app = "com.google.android.tvlauncher"
    
    #LOG
    self.log("State changed: " + str(old) + " @ " + self.translate_app(self.old_app) + " > " + str(new) + " @ " + self.translate_app(current_app))
    
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
      if (self.is_app_controling_lights(self.old_app) or self.is_app_controling_lights(current_app)):
        #CALL SCRIPT
        self.log("TV stopped : Lights fully un-dimmed")
        self.call_service("script/lights_set_livingroom_kitchen_regular")
      
    self.old_app = current_app

  """


  """
  def callback_ps5_state_change(self, entity, attribute, old, new, kwargs):
    if old in ["off" , None] and new == 'on':
        self.log("PS5 is use : Lights dimmed")
        self.call_service("script/lights_set_tv") 
    elif old == "on" and new == 'off':
        self.log("PS5 stopped : Lights fully un-dimmed")
        self.call_service("script/lights_set_livingroom_kitchen_regular")

  """
  Helper method:
  Does : 
  . nothing
  Returns : true if an app is controlling the light, false otherwise
  """
  def is_app_controling_lights(self, tv_app):
    supported_app_ids = [ 
      "com.netflix.ninja",
      "com.amazon.amazonvideo.livingroom",
      "com.plexapp.android"]
    if tv_app in supported_app_ids:
      return True
    else:
      return False

  """
  Helper method:
  Does : 
  . nothing
  Returns : A human readable format of the app_id if known (the app_id otherwise)
  """
  def translate_app(self, tv_app):
    translations = {
      "com.netflix.ninja":"Netflix",
      "com.amazon.amazonvideo.livingroom":"Amazon Prime",
      "com.plexapp.android":"Plex",
      "tv.molotov.app":"Molotov",
      "com.google.android.tvlauncher":"Home",
      "com.spotify.tv.android":"Spotify",
      "com.google.android.youtube.tv":"YouTube",
      "com.google.android.apps.mediashell":"Cast",
      "com.aspiro.tidal":"Tidal",
      "org.droidtv.playtv": "HDMI Output",
      "org.droidtv.channels": "Source Selector"
    }
    if tv_app in translations:
      return translations[tv_app]
    else:
      return tv_app

