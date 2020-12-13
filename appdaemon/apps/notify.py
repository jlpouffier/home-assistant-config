import hassapi as hass

"""
Notify is a smart notification hub notifying important events.
Notifications
. Coming from clean_house:
  . Spiroo will start > Cancel possible
  . Spiroo is starting > RTH possible
  . Spiroo is in error with location and error label
  . Spiroo has finished cleaning with stats and map of cleaned area
  . Spiroo not docked for more than 30 minutes
. Coming from monitor_home
  . Notify lights are still on when nobody is at home > Turn off light possible
  . Notify TV still on when nobody is at home > Turn off TV possible
  . Notify AC still on when nobody is at home > Turn off AC possible
. Coming from watch_tv
  . Notify that the lights are driven by the TV > turn off possible
  . Notify that the lights are not driven by the TV > turn on possible
. Coming directly from here
  . Notify HASS update

"""
class notify(hass.Hass): 
  def initialize(self):
    # State change : Update available
    self.listen_state(self.callback_hass_update_available, "binary_sensor.updater" , old = "off" , new = "on")
    
    # NOTIFY events from clean_house
    self.listen_event(self.callback_notify_cleaning_scheduled , "NOTIFY", payload = "cleaning_scheduled")
    self.listen_event(self.callback_notify_cleaning_started , "NOTIFY", payload = "cleaning_started")
    self.listen_event(self.callback_notify_cleaning_finished , "NOTIFY", payload = "cleaning_finished")
    self.listen_event(self.callback_notify_cleaning_error , "NOTIFY", payload = "cleaning_error")
    self.listen_event(self.callback_notify_cleaning_idle , "NOTIFY", payload = "cleaning_idle")

    # NOTIFY events from watch_tv
    self.listen_event(self.callback_notify_watch_tv_on , "NOTIFY", payload = "watch_tv_on")
    self.listen_event(self.callback_notify_watch_tv_off , "NOTIFY", payload = "watch_tv_off")

    # NOTIFY events from monitor_home
    self.listen_event(self.callback_notify_lights_still_on , "NOTIFY", payload = "lights_still_on")
    self.listen_event(self.callback_notify_tv_still_on , "NOTIFY", payload = "tv_still_on")
    self.listen_event(self.callback_notify_climate_still_on , "NOTIFY", payload = "climate_still_on")

    # Button clicked events
    self.listen_event(self.callback_button_clicked_rth_spiroo, "mobile_app_notification_action", action = "rth_spiroo")
    self.listen_event(self.callback_button_clicked_turn_off_lights, "mobile_app_notification_action", action = "turn_off_lights")
    self.listen_event(self.callback_button_clicked_turn_off_tv, "mobile_app_notification_action", action = "turn_off_tv")
    self.listen_event(self.callback_button_clicked_turn_off_climate, "mobile_app_notification_action", action = "turn_off_climate")
    self.listen_event(self.callback_button_clicked_cancel_planned_clean_house, "mobile_app_notification_action", action = "cancel_planned_clean_house")
    self.listen_event(self.callback_button_clicked_turn_off_watch_tv, "mobile_app_notification_action", action = "turn_off_watch_tv")
    self.listen_event(self.callback_button_clicked_turn_on_watch_tv, "mobile_app_notification_action", action = "turn_on_watch_tv")
    
    # log
    self.log("Notify bot initialized")


  """
  Callback triggered when a new version of HASS is available.
  Goals :
  . Notify (If the version number can be fetched : Include it in the notification)
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
  Callback triggered when event NOTIFY with payload "cleaning_scheduled" is received
  Goals :
  . Send notification
  """
  def callback_notify_cleaning_scheduled(self, event_name, data, kwargs):
    self.send_actionable_notification(
      title = "⏰ Nettoyage plannifié", 
      message = "Spiroo démarrera son nettoyage dans 30 minutes", 
      action_callback="cancel_planned_clean_house",
      action_title="Annuler le nettoyage",
      clickURL="/lovelace/bureau",
      timeout = 300)

  """
  Callback triggered when event NOTIFY with payload "cleaning_started" is received
  Goals :
  . Send notification
  """
  def callback_notify_cleaning_started(self, event_name, data, kwargs):
    self.send_actionable_notification(
      title = "🧹 Nettoyage", 
      message = "Spiroo démarre son nettoyage", 
      action_callback="rth_spiroo",
      action_title="Arrêter Spiroo",
      clickURL="/lovelace/bureau")

  """
  Callback triggered when event NOTIFY with payload "cleaning_finished" is received
  Goals :
  . Send notification
  """
  def callback_notify_cleaning_finished(self, event_name, data, kwargs):
    area_cleaned = self.get_state("sensor.spiroo_last_cleaning_area")
    cleaned_map = self.args["hass_base_url"] + self.get_state("camera.spiroo_cleaning_map" , attribute = "entity_picture")
    self.send_actionable_notification(
      title = "✅ Nettoyage terminé",
      message = "Surface nettoyée: " + area_cleaned + "m2",
      image = cleaned_map,
      clickURL = "/lovelace/bureau")

  """
  Callback triggered when event NOTIFY with payload "cleaning_error" is received
  Goals :
  . Send notification
  """
  def callback_notify_cleaning_error(self, event_name, data, kwargs):
    current_location = self.args["hass_base_url"] + self.get_state("camera.spiroo_cleaning_map" , attribute = "entity_picture")
    status = self.translate_spiroo_error_status(self.get_state("vacuum.spiroo" , attribute = "status"))
    self.send_actionable_notification(
      title = "⚠️ Spiroo est en erreur",
      message = status,
      image = current_location,
      clickURL = "/lovelace/bureau")

  """
  Callback triggered when event NOTIFY with payload "cleaning_idle" is received
  Goals :
  . Send notification
  """
  def callback_notify_cleaning_idle(self, event_name, data, kwargs):
    self.send_actionable_notification(
      title = "⚠️ Spiroo se décharge",
      message = "Je detecte que Spiroo n'est plus sur sa base depuis plus de 30 minutes",
      clickURL = "/lovelace/bureau")

  """
  Callback triggered when event NOTIFY with payload "watch_tv_on" is received
  Goals :
  . Send notification
  """
  def callback_notify_watch_tv_on(self, event_name, data, kwargs):
    self.send_actionable_notification(
      title = "📺 TV intelligente", 
      message = "La TV intelligente est activée", 
      action_callback="turn_off_watch_tv",
      action_title="Annuler",
      clickURL="/lovelace/bureau",
      timeout = 10)

  """
  Callback triggered when event NOTIFY with payload "watch_tv_off" is received
  Goals :
  . Send notification
  """
  def callback_notify_watch_tv_off(self, event_name, data, kwargs):
    self.send_actionable_notification(
      title = "📺 TV intelligente", 
      message = "La TV intelligente n'est pas activée", 
      action_callback="turn_on_watch_tv",
      action_title="Activer",
      clickURL="/lovelace/bureau",
      timeout = 10)

  """
  Callback triggered when event NOTIFY with payload "lights_still_on" is received
  Goals :
  . Send notification
  """
  def callback_notify_lights_still_on(self, event_name, data, kwargs):
    self.send_actionable_notification(
      title = "💡 Lumières allumées", 
      message = "Des lumières sont allumées alors que personne n'est présent", 
      action_callback="turn_off_lights",
      action_title="Éteindre les lumières",
      clickURL="/lovelace/salon")

  """
  Callback triggered when event NOTIFY with payload "tv_still_on" is received
  Goals :
  . Send notification
  """
  def callback_notify_tv_still_on(self, event_name, data, kwargs):
    self.send_actionable_notification(
      title = "📺 TV allumée", 
      message = "La TV est allumée alors que personne n'est présent", 
      action_callback="turn_off_tv",
      action_title="Éteindre la TV",
      clickURL="/lovelace/salon")

  """
  Callback triggered when event NOTIFY with payload "climate_still_on" is received
  Goals :
  . Send notification
  """
  def callback_notify_climate_still_on(self, event_name, data, kwargs):
    self.send_actionable_notification(
      title = "🧊 Clim allumée", 
      message = "Au moins une climatisation est allumée alors que personne n'est présent", 
      action_callback="turn_off_climate",
      action_title="Éteindre la Clim",
      clickURL="/lovelace/salon")

  """
  Callback triggered when button "" is clicked from a notification
  Goals :
  . 
  """
  def callback_button_clicked_rth_spiroo(self, event_name, data, kwargs):
    self.log("Notification button clicked : RTH Spirro") 
    self.call_service("vacuum/return_to_base" , entity_id = "vacuum.spiroo")

  """
  Callback triggered when button "turn_off_lights" is clicked from a notification
  Goals :
  . Turn off interior lights
  . Turn off exterior lights
  """
  def callback_button_clicked_turn_off_lights(self, event_name, data, kwargs):
    self.log("Notification button clicked : Turning off lights") 
    self.call_service("light/turn_off" , entity_id = "light.interior_lights")
    self.call_service("light/turn_off" , entity_id = "light.exterior_lights")

  """
  Callback triggered when button "turn_off_tv" is clicked from a notification
  Goals :
  . Turn off TV
  """
  def callback_button_clicked_turn_off_tv(self, event_name, data, kwargs):
    self.log("Notification button clicked : Turning off TV") 
    self.call_service("media_player/turn_off" , entity_id = "media_player.philips_android_tv")

  """
  Callback triggered when button "turn_off_climate" is clicked from a notification
  Goals :
  . Turn off climate
  """
  def callback_button_clicked_turn_off_climate(self, event_name, data, kwargs):
    self.log("Notification button clicked : Turning off climate")
    if self.get_state("climate.salon") != "off":
      self.call_service("climate/turn_off" , entity_id = "climate.salon")
      
    if self.get_state("climate.chambre") != "off":
      self.call_service("climate/turn_off" , entity_id = "climate.chambre")
      
    if self.get_state("climate.bureau") != "off":
      self.call_service("climate/turn_off" , entity_id = "climate.bureau")


  """
  Callback triggered when button "cancel_planned_clean_house" is clicked from a notification
  Goals :
  . Send event CANCEL_AUTOMATION with paylaod "clean_house". See app clean_house for more details.
  """
  def callback_button_clicked_cancel_planned_clean_house(self, event_name, data, kwargs):
    self.log("Notification button clicked : canceling scheduled cleaning") 
    self.fire_event("CANCEL_AUTOMATION", payload = "clean_house")

  """
  Callback triggered when button "turn_off_watch_tv" is clicked from a notification
  Goals :
  . turn off watch_tv automations
  . turn on Snips
  . Undim lights
  """
  def callback_button_clicked_turn_off_watch_tv(self, event_name, data, kwargs):
    self.log("Notification button clicked : Turning off watch_tv automations") 
    self.call_service("input_boolean/turn_off", entity_id = "input_boolean.watch_tv_automation_switch")
    self.call_service("script/lights_set_livingroom_kitchen_regular") 
    self.call_service("input_boolean/turn_on", entity_id = "input_boolean.snips_switch")

  """
  Callback triggered when button "turn_on_watch_tv" is clicked from a notification
  Goals :
  . turn on watch_tv automations
  . turn off Snips
  . Dim lights
  """
  def callback_button_clicked_turn_on_watch_tv(self, event_name, data, kwargs):
    self.log("Notification button clicked : Turning on watch_tv automations") 
    self.call_service("input_boolean/turn_on", entity_id = "input_boolean.watch_tv_automation_switch")
    self.call_service("script/lights_set_tv") 
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
    
