import hassapi as hass

"""
watch_tv is an app that listen to state changes of Android TV and dim the lights accordingly 
Functionalities :
. Dim lights when some apps are playing (only if sun is set)
. Undim lights partially when some apps are paused (only if sun is set)
. Undim lights totally when some apps are stopped (only if sun is set)
. Deactivcate Snips when some app are playing
. re-activate Snips when some apps are paused / stopped

List of apps driving Lights:
. Youtube
. Kodi
. Molotov

List of apps driving Snips
. Youtube
. kodi
. Molotiv
. Cast
. Spotify
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
  . Deactivcate Snips when some app are playing
  . re-activate Snips when some apps are paused / stopped
  """
  def callback_philips_android_tv(self, entity, attribute, old, new, kwargs):
    attr = self.get_state(entity, attribute = "all")
    if 'attributes' in attr and 'app_id' in attr["attributes"]:
      current_app = attr["attributes"]["app_id"] 
      # If the current app, or the old app are linked to the lights, and if the sun is set, change the lights depending on the states.
      if (self.is_app_controling_light(current_app) or self.is_app_controling_light(self.old_app)) and self.is_dark():
        if old in ["off", "standby", "unavailable" , "paused", "unknown", "idle"] and new == "playing":
          #CALL SCRIPT
          self.log("Setting lights to PLAYING mode :")
          self.log("[" + current_app + " > " + self.old_app + "] : " + old + " > " + new)
          self.call_service("script/lights_set_tv")  
        elif old == "playing" and new == "paused":
          #CALL SCRIPT
          self.log("Setting lights to PAUSED mode :")
          self.log("[" + current_app + " > " + self.old_app + "] : " + old + " > " + new)
          self.call_service("script/lights_set_tv_paused")
        elif old in ["playing" , "paused"] and new in ["standby" , "off" , "unavailable", "unknown", "idle"]:
          #CALL SCRIPT
          self.log("Setting lights to STOPPTED mode :")
          self.log("[" + current_app + " > " + self.old_app + "] : " + old + " > " + new)
          self.call_service("script/lights_set_livingroom_kitchen_regular") 

      # If the current app, or the old app are linked to the Snips, activate / deactivate Snips
      if self.is_app_controling_snips(current_app) or self.is_app_controling_snips(self.old_app):
        if old in ["off", "standby", "unavailable" , "paused", "unknown", "idle"] and new == "playing":
          #CALL SCRIPT
          self.log("TV playing : Snips OFF")
          self.log("[" + current_app + " > " + self.old_app + "] : " + old + " > " + new)
          self.call_service("input_boolean/turn_off", entity_id = "input_boolean.snips_switch")
        elif old == "playing" and new == "paused":
          #CALL SCRIPT
          self.log("TV paused : Snips ON")
          self.log("[" + current_app + " > " + self.old_app + "] : " + old + " > " + new)
          self.call_service("input_boolean/turn_on", entity_id = "input_boolean.snips_switch")
        elif old in ["playing" , "paused"] and new in ["standby" , "off" , "unavailable", "unknown", "idle"]:
          #CALL SCRIPT
          self.log("TV stopped : Snips ON")
          self.log("[" + current_app + " > " + self.old_app + "] : " + old + " > " + new)
          self.call_service("input_boolean/turn_on", entity_id = "input_boolean.snips_switch")

      self.old_app = current_app
  
  """
  Helper method:
  Does : Nothing
  Returns :  True if the app is part of the supported list of app linked to lights and False otherwise
  """
  def is_app_controling_light(self, app_id):
    supported_app_ids = ["org.xbmc.kodi", "com.google.android.youtube.tv", "tv.molotov.app", "com.netflix.ninja"]
    if app_id in supported_app_ids:
      return True
    else:
      return False

  """
  Helper method:
  Does : Nothing
  Returns :  True if the app is part of the supported list of app linked to Snips and False otherwise
  """
  def is_app_controling_snips(self, app_id):
    supported_app_ids = ["org.xbmc.kodi", "com.google.android.youtube.tv", "tv.molotov.app", "com.netflix.ninja" , "com.google.android.apps.mediashell", "com.spotify.tv.android"]
    if app_id in supported_app_ids:
      return True
    else:
      return False

  """
  Helper method:
  Does : Nothing
  Returns :  True it is dark outside, False otherwise
  """
  def is_dark(self):
    if self.get_state("sun.sun") == "below_horizon":
      return True
    else:
      return False

