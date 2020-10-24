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
    self.listen_event(self.callback_notify_event , "NOTIFY")
    self.listen_state(self.callback_hass_update_available, "binary_sensor.updater" , old = "off" , new = "on")
    self.listen_event(self.callback_notification_button_clicked, "mobile_app_notification_action")
    
    self.log("Notify bot initialized")


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



  def callback_notify_event(self, event_name, data, kwargs):
    payload = data["payload"] 
    self.log("Received notify event : " + payload)

    # notification coming from clean_house
    if payload == "cleaning_scheduled":
      self.send_actionable_notification(
        title = "⏰ Nettoyage plannifié", 
        message = "Spiroo démarrera son nettoyage dans 30 minutes", 
        action_callback="cancel_planned_clean_house",
        action_title="Annuler le nettoyage",
        clickURL="/lovelace-rooms/bureau",
        timeout = 300)

    elif payload == "cleaning_started":
      self.send_actionable_notification(
        title = "🧹 Nettoyage", 
        message = "Spiroo démarre son nettoyage", 
        action_callback="rth_spiroo",
        action_title="Arrêter Spiroo",
        clickURL="/lovelace-rooms/bureau")

    elif payload == "cleaning_finished":
      area_cleaned = self.get_state("sensor.spiroo_last_cleaning_area")
      cleaned_map = self.args["hass_base_url"] + self.get_state("camera.spiroo_cleaning_map" , attribute = "entity_picture")
      self.send_actionable_notification(
        title = "✅ Nettoyage terminé",
        message = "Surface nettoyée: " + area_cleaned + "m2",
        image = cleaned_map,
        clickURL = "/lovelace-rooms/bureau")

    elif payload == "cleaning_error":
      current_location = self.args["hass_base_url"] + self.get_state("camera.spiroo_cleaning_map" , attribute = "entity_picture")
      status = self.translate_spiroo_error_status(self.get_state("vacuum.spiroo" , attribute = "status"))
      self.send_actionable_notification(
        title = "⚠️ Spiroo est en erreur",
        message = status,
        image = current_location,
        clickURL = "/lovelace-rooms/bureau")

    elif payload == "cleaning_idle":
      self.send_actionable_notification(
        title = "⚠️ Spiroo se décharge",
        message = "Je detecte que Spiroo n'est plus sur sa base depuis plus de 30 minutes",
        clickURL = "/lovelace-rooms/bureau")



    # notification coming from watch_tv
    elif payload == "watch_tv_on":
      self.send_actionable_notification(
        title = "📺 TV intelligente", 
        message = "La TV intelligente est activée", 
        action_callback="turn_off_watch_tv",
        action_title="Annuler",
        clickURL="/lovelace-rooms/bureau",
        timeout = 10)
    elif payload == "watch_tv_off":
      self.send_actionable_notification(
        title = "📺 TV intelligente", 
        message = "La TV intelligente n'est pas activée", 
        action_callback="turn_on_watch_tv",
        action_title="Activer",
        clickURL="/lovelace-rooms/bureau",
        timeout = 10)



    # notification coming from monitor_house
    elif payload == "lights_still_on":
      self.send_actionable_notification(
        title = "💡 Lumières allumées", 
        message = "Des lumières sont allumées alors que personne n'est présent", 
        action_callback="turn_off_lights",
        action_title="Éteindre les lumières",
        clickURL="/lovelace-rooms/salon")
    
    elif payload == "tv_still_on":
      self.send_actionable_notification(
        title = "📺 TV allumée", 
        message = "La TV est allumée alors que personne n'est présent", 
        action_callback="turn_off_tv",
        action_title="Éteindre la TV",
        clickURL="/lovelace-rooms/salon")
    
    elif payload == "climate_still_on":
      self.send_actionable_notification(
        title = "🧊 Clim allumée", 
        message = "La climatisation est allumée alors que personne n'est présent", 
        action_callback="turn_off_climate",
        action_title="Éteindre la Clim",
        clickURL="/lovelace-rooms/salon")
    


  """
  Callback triggered when Notify receives a mobile_app_notification_action from a button click on a notification
  Supported actions
  . rth_spiroo (RTH spiroo)
  . turn_off_lights (Turn off all lights)
  . turn_off_tv (Turn of TV)
  . turn_off_climate (Turn of climate)
  . cancel_planned_clean_house (Cancel the incomming Spiroo start)
  """
  def callback_notification_button_clicked(self, event_name, data, kwargs):
    payload = data["action"]
    self.log("A notification button is clicked: " + payload)
    
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
    
