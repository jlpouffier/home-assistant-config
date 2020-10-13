import hassapi as hass

"""
Edith is telegram chat bot notifying important events.
Functionalities
. Turn herself on and off based on home assistant switch edith_switch
. Notify Spiroo will start > Cancel possible
. Notify Spiroo is starting > RTH possible (Return to home)
. Notify Spiroo is in error with location and error label (TODO)
. Notify Spiroo has finished cleaning with stats and map of cleaned area
. Nofify Spiroo not docked for more than 30 minutes
. Notify HASS update
. Notify lights are still on when nobody is at home > Turn off light possible
. Notify TV still on when nobody is at home > Turn off TV possible
. Reply to /ping command wih /pong
. Reply to /pong command with /ping
. Reply to /restart command > Confirm mandatory 
"""
class edith(hass.Hass): 
  def initialize(self):
    self.listen_state(self.callback_toggle_edith, "input_boolean.edith_switch")
    self.state_handles = []
    self.event_handles = []

    # Only register Edith if the Home assistant Switch is ON. Prevent weird start-up
    if self.get_state("input_boolean.edith_switch") == 'on':
      self.register_edith()

    self.log("Edith bot initialized")

  '''
  Callback triggered when Edith main switch change state
  Goals :
  . Register and Unregister all callbacks associated to Edith
  '''
  def callback_toggle_edith(self, entity, attribute, old, new, kwargs):
    if old != new:
      if new == 'on':
        self.log("Edith turned on")
        self.register_edith()
      if new == 'off':
        self.unregister_edith()
        self.log("Edith turned off") 

  """
  Helper method:
  Does : Register Edith to all neccesary callbacks
         Send a telegram message, but only if it' s not initialization (To avoid constant ping when developping)
  Returns :  Nothing
  """
  def register_edith(self):
    # SPIROO CALLBACKS
    self.state_handles.append(self.listen_state(self.callback_spiroo_stated, "vacuum.spiroo" , old = "docked" , new = "cleaning"))
    self.state_handles.append(self.listen_state(self.callback_spiroo_finished, "vacuum.spiroo" , old = "paused" , new = "docked"))
    self.state_handles.append(self.listen_state(self.callback_spiroo_finished, "vacuum.spiroo" , old = "cleaning" , new = "docked"))
    self.state_handles.append(self.listen_state(self.callback_spiroo_finished, "vacuum.spiroo" , old = "returning" , new = "docked"))
    self.state_handles.append(self.listen_state(self.callback_spiroo_error, "vacuum.spiroo" , new = "error"))
    self.state_handles.append(self.listen_state(self.callback_spiroo_idle, "vacuum.spiroo" , new = "idle" , duration = 1800))

    # DELAYED AUTOMATION CALLBACK
    self.event_handles.append(self.listen_event(self.callback_delayed_automation_receveived , "DELAYED_AUTOMATION_NOTIFICATION"))

    # HASS CALLBACKS
    self.state_handles.append(self.listen_state(self.callback_hass_update_available, "binary_sensor.updater" , old = "off" , new = "on"))

    # HOME CALLBACKS
    self.state_handles.append(self.listen_state(self.callback_home_empty , "binary_sensor.home_occupied" , old = "on" , new = "off"))

    # TELEGRAM CALLBACK
    self.event_handles.append(self.listen_event(self.callback_telegram_command_received, "telegram_command"))
    self.event_handles.append(self.listen_event(self.callback_telegram_callback_received, "telegram_callback"))
 

  """
  Helper method:
  Does : Unregister Edith to all associated callbacks
  Returns :  Nothing
  """
  def unregister_edith(self):
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
  . Expose actions to either acknowledge or RTH Spiroo
  """
  def callback_spiroo_stated(self, entity, attribute, old, new, kwargs):
    self.log("Detecting that Spiroo is starting. Notifying it...")
    # Send message with two telegram_callbacks
    # /ack : acknowledge Spiroo start
    # /rth_spiroo : RTH Spiroo
    self.call_service("telegram_bot/send_message", message = "Spiroo démarre son nettoyage ..." , inline_keyboard = ["C'est normal:/ack" , "Annule le nettoyage:/rth_spiroo"])


  """
  Callback triggered when Spiroo finish cleaning (state change : [paused, cleaning, returning] > docked)
  Goals :
  . Notify
  . Send stats (Curent batery level & Area cleaned)
  . Send map of cleaned area
  """
  def callback_spiroo_finished(self, entity, attribute, old, new, kwargs):
    self.log("Detecting that Spiroo has finished. Notifying it...")
    # Retrieve spiroo usefull states
    area_cleaned = self.get_state("sensor.spiroo_last_cleaning_area")
    current_battery_level = self.get_state("sensor.spiroo_battery_level")
    cleaned_map = self.args["hass_base_url"] + self.get_state("camera.spiroo_cleaning_map" , attribute = "entity_picture")
    # Send summary message
    self.call_service("telegram_bot/send_message", message = "Spiroo a terminé son nettoyage")
    # Send stats message
    self.call_service("telegram_bot/send_message", message = "Surface nettoyée: " + area_cleaned + "m2")
    self.call_service("telegram_bot/send_message", message = "Niveau de batterie actuel: " + current_battery_level + "%")
    # Send map
    self.call_service("telegram_bot/send_photo", url = cleaned_map)


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
      self.call_service("telegram_bot/send_message", message = "Spiroo est en erreur :")
      self.call_service("telegram_bot/send_message", message = status)
      # Send map
      self.call_service("telegram_bot/send_photo", url = current_location)


  """
  Callback triggered when Spiroo is not docked for more than 30 minutes
  Goals :
  . Notify
  """
  def callback_spiroo_idle(self, entity, attribute, old, new, kwargs):
    if old != new:
      self.log("Detecting that Spiroo is not plugged since more than 30 miuntes. Notifying it...")
      # Send message
      self.call_service("telegram_bot/send_message", message = "Je detecte que Spiroo n' est plus sur sa base depuis plus de 30 minutes ...")


  """
  Callback triggered when a new version of HASS is available.
  Goals :
  . Notify (If the version number can be fetch : Include it in the notification)
  """
  def callback_hass_update_available(self, entity, attribute, old, new, kwargs):
    self.log("Detecting an available update for HASS. Notifying it...")
    # Retreive home assistant version
    version = self.get_state("binary_sensor.updater", attribute = "newest_version")
    # Send message
    if version is None:
      self.call_service("telegram_bot/send_message", message = " Nouvelle version de Home Assistant est dispo ! (Version inconnue)")
    else:
      self.call_service("telegram_bot/send_message", message = " La version " + version + " de Home Assistant est dispo !")


  """
  Callback triggered wehn the home becomes empty. A test will be made to check if lights are still on
  Goals :
  . Notify
  . Expose actions to either acknowledge or turn ligts off
  """
  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    # test if lights are still on
    if self.get_state("light.interior_lights") == "on":
      self.log("Detecting home empty and lights on. Notifying it...")
      # fetch all lights turned on
      lights_on = self.get_lights_turned_on()
      # Send message with two telegram_callbacks
      # /ack : acknowlege lights are still on
      # /turn_off_lights : turn off lights
      self.call_service("telegram_bot/send_message", message = "Je détecte encore des lumières allumées alors que personne n'est présent:\n\n" + "\n".join(lights_on), inline_keyboard = ["C'est normal:/ack" , "Éteins les lumières:/turn_off_lights"])

    # test if TV is still on
    if self.get_state("media_player.philips_android_tv") not in ["off", "standby", "unavailable"]:
      self.log("Detecting home empty and TV on. Notifying it...")
      # Send message with two telegram_callbacks
      # /ack : acknowlege TV is still on
      # /turn_off_tv : turn off TV
      self.call_service("telegram_bot/send_message", message = "Je détecte encore la TV allumée alors que personne n'est présent", inline_keyboard = ["C'est normal:/ack" , "Éteins la TV:/turn_off_tv"])




  """
  Callback triggered when Edith receives a telegram_command (ie. /command)
  Supported Commands
  . /ping (reply with /pong)
  . /pong (reply with /ping)
  . /restart (ask for confirmation and potentially restart HASS
  . Any other command will be replied with a default error message)
  """
  def callback_telegram_command_received(self, event_name, data, kwargs):
    cmd = data["command"] 
    self.log("A telegram command is received : " + cmd)
    if cmd.lower() == "/ping":
      # Send message
      self.call_service("telegram_bot/send_message", message = "/pong")
    elif cmd.lower() == "/pong":
      # Send message
      self.call_service("telegram_bot/send_message", message = "/ping")
    elif cmd.lower() == "/restart":
      # Send message with two telegram_callbacks
      # /ack : Does nothing
      # /restart_hass : Restart HASS
      self.call_service("telegram_bot/send_message", message = "Sûr ?" , inline_keyboard = ["Oui:/restart_hass", "Non:/ack"])
    elif cmd.lower() == '/say':
      if data['args']:
        payload = ""
        for arg in data['args']:
          payload += arg
          payload += " "
        self.fire_event("SNIPS_SAY", payload = payload)
    else:
      # Send generic unsupported message
      self.call_service("telegram_bot/send_message", message = "Commande " + data["command"] + " non supportée ...")


  """
  Callback triggered when Edith receives a telegram_callback from an inline keyboard 
  Supported callback
  . /ack (do nothing)
  . /rth_spiroo (RTH spiroo)
  . /turn_off_lights (Turn off all lights)
  . /restart_hass (Restart HASS)
  . /cancel_planned_clean_house (Cancel the incomming Spiroo start)
  """
  def callback_telegram_callback_received(self, event_name, data, kwargs):
    payload = data["data"]
    self.log("A telegram callback is received : " + payload)
    self.reply_telegram_callback(data)
    if payload == "/rth_spiroo":
      # RTH Spiroo
      self.call_service("vacuum/return_to_base" , entity_id = "vacuum.spiroo")
    elif payload == "/turn_off_lights":
      # Turn off all lights
      self.call_service("light/turn_off" , entity_id = "light.interior_lights")
      self.call_service("light/turn_off" , entity_id = "light.exterior_lights")
    elif payload == "/turn_off_tv":
      # Turn off TV
      self.call_service("media_player/turn_off" , entity_id = "media_player.philips_android_tv")
    elif payload == "/restart_hass":
      # Restart HASS
      self.call_service("homeassistant/restart")
    elif payload == "/cancel_planned_clean_house":
      # Send event DELAYED_AUTOMATION_CANCELED with payload = clean_house (See clean_house app that will receive it)
      self.fire_event("DELAYED_AUTOMATION_CANCELED", payload = "clean_house")


  """
  Callback triggered when Edith receives the event DELAYED_AUTOMATION_NOTIFICATION.
  This event is fired by other app that will soon starts automation.
  Edith can cancel these automation thanks to that callback
  Supported :
  . usecase_manager.clean_house sending DELAYED_AUTOMATION_NOTIFICATION with payload clean_house 30 minutes before Spiroo cleaning.
  """
  def callback_delayed_automation_receveived(self, event_name, data, kwargs):
    payload = data["payload"]
    self.log("Received a delayed automation notification : " + payload)
    if payload == "clean_house":
      # Send message
      self.call_service("telegram_bot/send_message", message = "Spiroo démarrera son nettoyage dans 30 minutes" , inline_keyboard = ["Ok:/ack", "Annuler:/cancel_planned_clean_house"])


  """
  Helper method:
  Does : Nothing
  Returns :  All rooms that are turned on
  """
  def get_lights_turned_on(self):
    output = []
    # List of rooms
    rooms = [
      "light.cuisine",
      "light.salon",
      "light.entree",
      "light.chambre_principale",
      "light.chambre_secondaire",
      "light.terrasse"
    ]

    for room in rooms:
      if self.get_state(room) == "on":
        output.append(self.get_state(room, attribute = 'friendly_name'))

    return output


  """
  Helper method:
  Does : 
  . Reply to the telegram_callback linked ot the data received in input with a generic message 
  Returns : Nothing

  """
  def reply_telegram_callback(self, data):
    # Remove inline keyboard options
    self.delete_inline_keyboard(data)
    # Reply to telegram_callback
    self.call_service("telegram_bot/answer_callback_query" , callback_query_id = data["id"], message = "C'est noté")

  """
  Helper method:
  Does : 
  . Remove the inline keyboard options linked to the data received in input
  Returns : Nothing

  """
  def delete_inline_keyboard(self, data):
    # Remove inline keyboard options
    self.call_service("telegram_bot/edit_replymarkup" , message_id = data["message"]["message_id"] , chat_id = data["message"]["chat"]["id"], inline_keyboard = [])

  """
  Helper method:
  Does : 
  . Translate known English status in French
  Returns : the translated status

  """
  def translate_spiroo_error_status(self, status):
    translations = {
        "Dust bin missing":"Veuillez remettre mon bac à poussière",
        "Picked up":"Merci de me remettre sur le sol",
        "Docked":"Je suis sur ma base ...",
        "Clear my path":"Dégagez mon chemin",
        "Brush stuck":"Nettoyer ma brosse"
    }
    if status in translations:
      return translations[status]
    else:
      return status
    




