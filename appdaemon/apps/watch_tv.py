import hassapi as hass

"""
watch_tv is an app that listen to state changes of Android TV and dim the lights accordingly 
Functionalities :
. Dim lights when some apps are playing (only if sun is set)
. Undim lights partially when some apps are paused (only if sun is set)
. Undim lights totally when some apps are stopped (only if sun is set)

List of apps driving Lights:
. Netflix
. Plex
. Amazon Prime

"""
class watch_tv(hass.Hass):
  def initialize(self):
    # TV CALLBACK
    self.listen_state(self.callback_philips_android_tv, "media_player.philips_android_tv")

    # PS5 Callback
    self.listen_state(self.callback_ps5, "binary_sensor.is_ps5_used")

    self.log("Watch TV Automation initialized")
    # Variable to store the old app to detect app changes. Initialized to the Android Home page
    self.old_app = "com.google.android.tvlauncher"

  """
  Callback trigerred every time Android TV state change
  Goals
  . Dim lights when some apps are playing
  . Undim lights partially when some apps are paused
  . Undim lights totally when some apps are stopped 
  """
  def callback_philips_android_tv(self, entity, attribute, old, new, kwargs):
    # Get attrobutes of the TV and fetch the current app
    attr = self.get_state(entity, attribute = "all")
    if 'attributes' in attr and 'app_id' in attr["attributes"]:
      current_app = attr["attributes"]["app_id"] 
    else:
      current_app = "com.google.android.tvlauncher"
    
    #LOG
    self.log("State changed: " + old + " @ " + self.translate_app(self.old_app) + " > " + new + " @ " + self.translate_app(current_app))
    
    if old in ["off", "standby", "unavailable" , "paused", "unknown", "idle"] and new == "playing":
      if self.is_app_controling_lights(current_app):
        #CALL SCRIPT
        self.log("TV playing : Lights dimmed")
        self.call_service("script/lights_set_tv")  
      
    elif old == "playing" and new == "paused":
      if self.is_app_controling_lights(current_app):
        #CALL SCRIPT
        self.log("TV paused : Lights partially un-dimmed")
        self.call_service("script/lights_set_tv_paused")        
 
    elif old in ["playing" , "paused"] and new in ["standby" , "off" , "unavailable", "unknown", "idle"]:
      if self.is_app_controling_lights(self.old_app) or self.is_app_controling_lights(current_app):
        #CALL SCRIPT
        self.log("TV stopped : Lights fully un-dimmed")
        self.call_service("script/lights_set_livingroom_kitchen_regular")
      
    self.old_app = current_app

  """
  Callback trigerred every time is_ps5_used changes
  Goals
  . Dim lights when ps5 used
  . Undim lights totally when when ps5 stopped
  """
  def callback_ps5(self, entity, attribute, old, new, kwargs):
    if new == 'on' and self.get_state("sun.sun") == "below_horizon":
        self.log("PS5 is use : Lights dimmed")
        self.call_service("script/lights_set_tv") 
    elif new == 'off' and self.get_state("sun.sun") == "below_horizon":
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
    if tv_app in supported_app_ids and self.get_state("sun.sun") == "below_horizon":
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
      "com.aspiro.tidal":"Tidal"
    }
    if tv_app in translations:
      return translations[tv_app]
    else:
      return tv_app

