import hassapi as hass

"""
Notify is a smart notification hub notifying important events.
Functionalities
. Turn itself on and off based on home assistant switch notify_switch
. Notify Spiroo will start > Cancel possible
. Notify Spiroo is starting > RTH possible (Return to home)
. Notify Spiroo is in error with location and error label
. Notify Spiroo has finished cleaning with stats and map of cleaned area
. Nofify Spiroo not docked for more than 30 minutes
. Notify HASS update
. Notify lights are still on when nobody is at home > Turn off light possible
. Notify TV still on when nobody is at home > Turn off TV possible
. Notify AC still on when nobody is at home > Turn off AC possible
"""
class notify(hass.Hass): 
  def initialize(self):
    self.listen_state(self.callback_toggle_notify, "input_boolean.notify_switch")
    self.state_handles = []
    self.event_handles = []

    # Only register Notify if the Home assistant Switch is ON. Prevent weird start-up
    if self.get_state("input_boolean.notify_switch") == 'on':
      self.register_notify()

    self.log("Notify bot initialized")

  '''
  Callback triggered when Notify main switch change state
  Goals :
  . Register and Unregister all callbacks associated to Notify
  '''
  def callback_toggle_notify(self, entity, attribute, old, new, kwargs):
    if old != new:
      if new == 'on':
        self.log("Notify turned on")
        self.register_notify()
      if new == 'off':
        self.unregister_notify()
        self.log("Notify turned off") 

  """
  Helper method:
  Does : Register Notify to all neccesary callbacks
  Returns :  Nothing
  """
  def register_notify(self):
    # SPIROO CALLBACKS
    self.state_handles.append(self.listen_state(self.callback_spiroo_stated, "vacuum.spiroo" , old = "docked" , new = "cleaning"))
    self.state_handles.append(self.listen_state(self.callback_spiroo_finished, "vacuum.spiroo" , old = "paused" , new = "docked"))
    self.state_handles.append(self.listen_state(self.callback_spiroo_finished, "vacuum.spiroo" , old = "cleaning" , new = "docked"))
    self.state_handles.append(self.listen_state(self.callback_spiroo_finished, "vacuum.spiroo" , old = "returning" , new = "docked"))
    self.state_handles.append(self.listen_state(self.callback_spiroo_error, "vacuum.spiroo" , new = "error"))
    self.state_handles.append(self.listen_state(self.callback_spiroo_idle, "vacuum.spiroo" , new = "idle" , duration = 1800))

    # NOTIFY CALLBACK
    self.event_handles.append(self.listen_event(self.callback_notify_from_other_app , "NOTIFY"))

    # HASS CALLBACKS
    self.state_handles.append(self.listen_state(self.callback_hass_update_available, "binary_sensor.updater" , old = "off" , new = "on"))

    # HOME CALLBACKS
    self.state_handles.append(self.listen_state(self.callback_home_empty , "binary_sensor.home_occupied" , old = "on" , new = "off"))
 
    # NOTIFICATION CALLBACK
    self.event_handles.append(self.listen_event(self.callback_notification_action_received, "mobile_app_notification_action"))

  """
  Helper method:
  Does : Unregister Notify to all associated callbacks
  Returns :  Nothing
  """
  def unregister_notify(self):
    for handle in self.state_handles:
        self.cancel_listen_state(handle)
    for handle in self.event_handles:
      self.cancel_listen_event(handle)
    self.state_handles = []
    self.event_handles = []

  """
  Callback triggered when Spiroo starts cleaning (state change : * > cleaning)
  Goals : 
  . Notify
  . Expose actions to RTH Spiroo
  """
  def callback_spiroo_stated(self, entity, attribute, old, new, kwargs):
    self.log("Detecting that Spiroo is starting. Notifying it...")
    # Send notification with one action
    # rth_spiroo : RTH Spiroo
    self.send_actionable_notification(
      title = "🧹 Nettoyage", 
      message = "Spiroo démarre son nettoyage", 
      action_callback="rth_spiroo",
      action_title="Arrêter Spiroo",
      clickURL="/lovelace-rooms/bureau")

  """
  Callback triggered when Spiroo finish cleaning (state change : [paused, cleaning, returning] > docked)
  Goals :
  . Notify
  . Send stats (Area cleaned)
  . Send map of cleaned area
  """
  def callback_spiroo_finished(self, entity, attribute, old, new, kwargs):
    self.log("Detecting that Spiroo has finished. Notifying it...")
    # Retrieve spiroo usefull states
    area_cleaned = self.get_state("sensor.spiroo_last_cleaning_area")
    cleaned_map = self.args["hass_base_url"] + self.get_state("camera.spiroo_cleaning_map" , attribute = "entity_picture")
    # Send notification
    self.send_actionable_notification(
      title = "✅ Nettoyage terminé",
      message = "Surface nettoyée: " + area_cleaned + "m2",
      image = cleaned_map,
      clickURL = "/lovelace-rooms/bureau")


  """
  Callback triggered when Spiroo is in error (state change : * > error)
  Goals :
  . Notify
  . Send error label
  . Send location
  """
  def callback_spiroo_error(self, entity, attribute, old, new, kwargs):
    if old != new:
      self.log("Detecting that Spiroo is in trouble. Notifying it...")
      # retrieve spiroo usefull states
      current_location = self.args["hass_base_url"] + self.get_state("camera.spiroo_cleaning_map" , attribute = "entity_picture")
      status = self.translate_spiroo_error_status(self.get_state("vacuum.spiroo" , attribute = "status"))
      # Send message
      self.send_actionable_notification(
        title = "⚠️ Spiroo est en erreur",
        message = status,
        image = current_location,
        clickURL = "/lovelace-rooms/bureau")

  """
  Callback triggered when Spiroo is not docked for more than 30 minutes
  Goals :
  . Notify
  """
  def callback_spiroo_idle(self, entity, attribute, old, new, kwargs):
    if old != new:
      self.log("Detecting that Spiroo is not plugged since more than 30 miuntes. Notifying it...")
      # Send message
      self.send_actionable_notification(
        title = "⚠️ Spiroo se décharge",
        message = "Je detecte que Spiroo n'est plus sur sa base depuis plus de 30 minutes",
        clickURL = "/lovelace-rooms/bureau")

  """
  Callback triggered when a new version of HASS is available.
  Goals :
  . Notify (If the version number can be fetch : Include it in the notification)
  """
  def callback_hass_update_available(self, entity, attribute, old, new, kwargs):
    self.log("Detecting an available update for HASS. Notifying it...")
    # Retreive home assistant version
    version = self.get_state("binary_sensor.updater", attribute = "newest_version")
    # Send notification
    if version is None:
      self.send_actionable_notification(
        title = "🎉 Mise a jour disponible",
        message = "Nouvelle version de Home Assistant est dispo !",
        clickURL = "/hassio/dashboard")
    else:
      self.send_actionable_notification(
        title = "🎉 Mise a jour disponible",
        message = "La version " + version + " de Home Assistant est dispo !",
        clickURL = "/hassio/dashboard")


  """
  Callback triggered when the home becomes empty. A test will be made to check if lights, tv, ac are still on
  Goals :
  . Notify
  . Expose actions to either acknowledge or turn lights, TV, AC off
  """
  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    # test if lights are still on
    if self.get_state("light.interior_lights") == "on":
      self.log("Detecting home empty and lights on. Notifying it...")
      # Send notification with one action
      # turn_off_lights : turn off lights
      self.send_actionable_notification(
        title = "💡 Lumières allumées", 
        message = "Des lumières sont allumées alors que personne n'est présent", 
        action_callback="turn_off_lights",
        action_title="Éteindre les lumières",
        clickURL="/lovelace-rooms/salon")

    # test if TV is still on
    if self.get_state("media_player.philips_android_tv") not in ["off", "standby", "unavailable"]:
      self.log("Detecting home empty and TV on. Notifying it...")
      # Send notification with one action
      # turn_off_tv : turn off TV
      self.send_actionable_notification(
        title = "📺 TV allumée", 
        message = "La TV est allumée alors que personne n'est présent", 
        action_callback="turn_off_tv",
        action_title="Éteindre la TV",
        clickURL="/lovelace-rooms/salon")

    # test if the climate control is still on
    if self.get_state("climate.salon") != "off":
      self.log("Detecting home empty and climate on. Notifying it...")
      # Send notification with one action
      # turn_off_climate : turn off climate
      self.send_actionable_notification(
        title = "🧊 Clim allumée", 
        message = "La climatisation est allumée alors que personne n'est présent", 
        action_callback="turn_off_climate",
        action_title="Éteindre la Clim",
        clickURL="/lovelace-rooms/salon")

  """
  Callback triggered when Notify receives the event NOTIFY.
  This event is fired by other app that will soon starts automation.
  Notify can cancel these automation thanks to that callback
  Supported :
  . usecase_manager.clean_house sending NOTIFY with payload clean_house 30 minutes before Spiroo cleaning.
  """
  def callback_notify_from_other_app(self, event_name, data, kwargs):
    payload = data["payload"]
    self.log("Received notify event : " + payload)
    if payload == "clean_house":
      # Send notification
      self.send_actionable_notification(
        title = "⏰ Nettoyage plannifié", 
        message = "Spiroo démarrera son nettoyage dans 30 minutes", 
        action_callback="cancel_planned_clean_house",
        action_title="Annuler le nettoyage",
        clickURL="/lovelace-rooms/bureau",
        timeout = 300)
    if payload == "watch_tv_on":
      # Send notification
      self.send_actionable_notification(
        title = "📺 TV intelligente", 
        message = "La TV intelligente est activée", 
        action_callback="turn_off_watch_tv",
        action_title="Annuler",
        clickURL="/lovelace-rooms/bureau",
        timeout = 10)
    if payload == "watch_tv_off":
      # Send notification
      self.send_actionable_notification(
        title = "📺 TV intelligente", 
        message = "La TV intelligente n'est pas activée", 
        action_callback="turn_on_watch_tv",
        action_title="Activer",
        clickURL="/lovelace-rooms/bureau",
        timeout = 10)


  """
  Callback triggered when Notify receives a mobile_app_notification_action from a button click on a notification
  Supported actions
  . rth_spiroo (RTH spiroo)
  . turn_off_lights (Turn off all lights)
  . turn_off_tv (Turn of TV)
  . turn_off_climate (Turn of climate)
  . cancel_planned_clean_house (Cancel the incomming Spiroo start)
  """
  def callback_notification_action_received(self, event_name, data, kwargs):
    payload = data["action"]
    self.log("A notification action is received : " + payload)
    if payload == "rth_spiroo":
      # RTH Spiroo
      self.call_service("vacuum/return_to_base" , entity_id = "vacuum.spiroo")
    elif payload == "turn_off_lights":
      # Turn off all lights
      self.call_service("light/turn_off" , entity_id = "light.interior_lights")
      self.call_service("light/turn_off" , entity_id = "light.exterior_lights")
    elif payload == "turn_off_tv":
      # Turn off TV
      self.call_service("media_player/turn_off" , entity_id = "media_player.philips_android_tv")
    elif payload == "turn_off_climate":
      # Turn off Climate
      self.call_service("climate/turn_off" , entity_id = "climate.salon")
    elif payload == "cancel_planned_clean_house":
      # Send event CANCEL_AUTOMATION with payload = clean_house (See clean_house app that will receive it)
      self.fire_event("CANCEL_AUTOMATION", payload = "clean_house")
    elif payload == "turn_off_watch_tv":
      # Turn off watch_tv_automation_switch
      self.call_service("input_boolean/turn_off", entity_id = "input_boolean.watch_tv_automation_switch")
      # Turn on lights
      self.call_service("script/lights_set_livingroom_kitchen_regular") 
      # Turn on Snips
      self.call_service("input_boolean/turn_on", entity_id = "input_boolean.snips_switch")
    elif payload == "turn_on_watch_tv":
      # Turn off watch_tv_automation_switch
      self.call_service("input_boolean/turn_on", entity_id = "input_boolean.watch_tv_automation_switch")
      # Turn on lights
      self.call_service("script/lights_set_tv") 
      # Turn off Snips
      self.call_service("input_boolean/turn_off", entity_id = "input_boolean.snips_switch")





  """
  Helper method:
  Does : 
  . Sends a Native notification to my phone based on the input parameters
  Returns : noting

  """
  def send_actionable_notification(self, title, message, clickURL = "", action_callback = "", action_title = "", image = "", timeout = 0):
    notification_data = {}
    if action_callback and action_title:
      notification_data["actions"] = [
        {
          "action":action_callback,
          "title":action_title
        }
      ]
    if image:
      notification_data["image"] = image
    if timeout != 0:
      notification_data["timeout"] = timeout
    if clickURL:
      notification_data["clickAction"] = clickURL
    self.call_service("notify/mobile_app_oneplus6t_app", title = title, message = message, data = notification_data)


  """
  Helper method:
  Does : 
  . Translate known English status in French
  Returns : the translated status

  """
  def translate_spiroo_error_status(self, status):
    translations = {
        "Dust bin missing":"Veuillez remettre mon bac à poussière",
        "Dust bin full":"Veuillez nettoyer mon bac à poussière",
        "Picked up":"Merci de me remettre sur le sol",
        "Docked":"Je suis sur ma base ...",
        "Clear my path":"Dégagez mon chemin",
        "Brush stuck":"Nettoyer ma brosse"
    }
    if status in translations:
      return translations[status]
    else:
      return status
    
