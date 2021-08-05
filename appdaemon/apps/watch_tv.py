import hassapi as hass

"""
watch_tv is an app that listen to state changes of Android TV and dim the lights accordingly 
Functionalities :
. Dim lights when some apps are playing (only if sun is set)
. Undim lights partially when some apps are paused (only if sun is set)
. Undim lights totally when some apps are stopped (only if sun is set)

List of apps driving Lights:
. Netflix
. Kodi
. Amazon Prime

"""
class watch_tv(hass.Hass):
  def initialize(self):
    # KODI CALLBACKS
    self.listen_state(self.callback_philips_android_tv, "media_player.philips_android_tv")
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
    self.log("[" + self.old_app + " > " + current_app + "] : " + old + " > " + new)
    
    if old in ["off", "standby", "unavailable" , "paused", "unknown", "idle"] and new == "playing":
      if self.is_controling_lights(self.old_app, current_app):
        #CALL SCRIPT
        self.log("TV playing : Lights dimmed")
        self.call_service("script/lights_set_tv")  
      
    elif old == "playing" and new == "paused":
      if self.is_controling_lights(self.old_app, current_app):
        #CALL SCRIPT
        self.log("TV paused : Lights partially un-dimmed")
        self.call_service("script/lights_set_tv_paused")        
 
    elif old in ["playing" , "paused"] and new in ["standby" , "off" , "unavailable", "unknown", "idle"]:
      if self.is_controling_lights(self.old_app, current_app):
        #CALL SCRIPT
        self.log("TV stopped : Lights fully un-dimmed")
        self.call_service("script/lights_set_livingroom_kitchen_regular")
      
    self.old_app = current_app
    
    
  """
  Helper method:
  Does : 
  . nothing
  Returns : true if an app is controlling the lightsm false otherwise

  """
  def is_controling_lights(self, old_tv_app, current_tv_app):
    supported_app_ids = [
      "org.xbmc.kodi", 
      "com.netflix.ninja",
      "com.amazon.amazonvideo.livingroom",
      "com.plexapp.android"]
    if (old_tv_app in supported_app_ids or current_tv_app in supported_app_ids) and self.get_state("sun.sun") == "below_horizon":
      return True
    else:
      return False

