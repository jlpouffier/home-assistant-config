import hassapi as hass
import datetime

"""
clean_house is an app responsible of the scheduling of TeuTeu and NeuNeu

Functionalities :
. Starts TeuTeu when needed 
. Handle cancelation of cleaning if requested

Notifications :
. Cleaning Scheduled > Start now or Cancel possible
. Cleaning Started > RTH possible
. Cleaning Finished
. TeuTeu error
. TeuTeu not on the dock
"""
class clean_house(hass.Hass):
  def initialize(self):
    self.listen_state(self.callback_home_empty_for_more_than_x_minutes, "binary_sensor.home_occupied", old = "on", nex= "off", duration = 600)
    self.listen_state(self.callback_teuteu_started, "vacuum.teuteu" , old = "docked" , new = "cleaning")
    self.listen_state(self.callback_teuteu_cleaning_for_more_than_x_minutes, "vacuum.teuteu" , new = "cleaning", duration = 900)
    self.listen_state(self.callback_teuteu_finished, "vacuum.teuteu",  new = "docked")
    self.listen_state(self.callback_teuteu_error, "vacuum.teuteu" , new = "error", immediate = True)
    self.listen_state(self.callback_teuteu_idle, "vacuum.teuteu" , new = "idle" , duration = 1800)
    
    #Listen to button press from notification
    self.listen_event(self.callback_button_clicked_cancel_planned_teuteu, "mobile_app_notification_action", action = "cancel_planned_teuteu")
    self.listen_event(self.callback_button_clicked_cancel_planned_teuteu_and_start_now, "mobile_app_notification_action", action = "cancel_planned_teuteu_and_start_now")
    self.listen_event(self.callback_button_clicked_rth_teuteu, "mobile_app_notification_action", action = "rth_teuteu")

    self.log("House cleaning Automation initialized")

  """
  Callback triggered when the home is empty for more than 30 minutes
  Goals :
  . Check if the last clean-up was done more then 36 hours ago
  . Check if we are not cleaning right now
  . If all 2 conditions are met:
    . Schedule cleaning in 30 minutes 
    . Send a notification
  """ 
  def callback_home_empty_for_more_than_x_minutes(self, entity, attribute, old, new, kwargs):
    self.log("Home empty for more than 10 minutes, checking if TeuTeu should clean the home now ... ")
    # Home concidered Dirty if last clean-up was done more then 36 hours ago
    now = self.datetime(True)
    last_cleaning = self.parse_datetime(self.get_state("input_datetime.dernier_nettoyage_de_teuteu"), aware = True) 
    diff = now - last_cleaning
    is_home_dirty = True if diff > datetime.timedelta(hours = 36) else False

    # Are we cleaning right now ?
    is_cleaning_right_now = True if self.get_state("vacuum.teuteu") == "cleaning" else False

    if is_home_dirty  and not is_cleaning_right_now:
      self.log("House cleaning will start in 30 minutes... Notifying it")
      delay = 1800
      # Schedule cleaning in 30 minutes via callback callback_cleaning
      self.cleaning_handle = self.run_in(self.callback_cleaning, delay)
      # Notify
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "⏰ Nettoyage plannifié", 
        message = "TeuTeu démarrera son nettoyage dans 30 minutes",
        callback = [{
          "title" : "Démarrer maintenant",
          "event" : "cancel_planned_teuteu_and_start_now"},{
          "title" : "Annuler le nettoyage",
          "event" : "cancel_planned_teuteu"}],
        click_url="/lovelace/teuteu",
        timeout = delay,
        icon = "mdi:robot-vacuum-variant")

  """
  Callback triggered 30 minutes after callback_home_empty_for_more_than_x_minutes if not cancelled
  Goals : 
  . Start TeuTeu
  """ 
  def callback_cleaning(self, kwargs):
    if self.get_state("binary_sensor.home_occupied") == 'on':
      self.log("House cleaning canceled : Home occupied")
    else:
      self.log("House cleaning will start now")
      # Start TeuTeu
      self.call_service("vacuum/start" , entity_id = "vacuum.teuteu")

  """
  Callback triggered when TeuTeu is starting
  Goals : 
  . Notify
  """   
  def callback_teuteu_started(self, entity, attribute, old, new, kwargs):
    self.log("Detecting that TeuTeu is starting. Notifying it...")
    self.fire_event("NOTIFIER",
      action = "send_to_nearest",
      title = "🧹 Nettoyage", 
      message = "TeuTeu démarre son nettoyage",
      callback = [{
        "title" : "Arrêter TeuTeu",
        "event" : "rth_teuteu"}],
      click_url="/lovelace/teuteu",
      icon = "mdi:robot-vacuum-variant")

  """
  Callback triggered when TeuTeu is cleaning for more than 15 minutes
  Goals : 
  . Update input_datetime.dernier_nettoyage_de_teuteu
  """   
  def callback_teuteu_cleaning_for_more_than_x_minutes(self, entity, attribute, old, new, kwargs):
    self.log("TeuTeu is cleaning since more than 15 minutes, updating the last clean-up datetime...")
    self.call_service("input_datetime/set_datetime", entity_id = "input_datetime.dernier_nettoyage_de_teuteu", datetime = self.datetime(True))

  """
  Callback triggered when TeuTeu is finished
  Goals : 
  . Notify
  """ 
  def callback_teuteu_finished(self, entity, attribute, old, new, kwargs):
    if old in ["paused", "cleaning", "returning"]:
      self.log("Detecting that TeuTeu has finished. Notifying it...")
      area_cleaned = self.get_state("sensor.teuteu_last_cleaning_area")
      cleaned_map = self.args["hass_base_url"] + self.get_state("camera.teuteu_cleaning_map" , attribute = "entity_picture")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "✅ Nettoyage terminé",
        message = "Surface nettoyée: " + area_cleaned + "m2",
        image_url = cleaned_map,
        click_url="/lovelace/teuteu",
        icon =  "mdi:robot-vacuum-variant",
        color = "#07ffc1")

  """
  Callback triggered when teuteu is in error
  Goals : 
  . Notify
  """ 
  def callback_teuteu_error(self, entity, attribute, old, new, kwargs):
    if old != new:
      self.log("Detecting that teuteu is in trouble. Notifying it...")
      current_location = self.args["hass_base_url"] + self.get_state("camera.teuteu_cleaning_map" , attribute = "entity_picture")
      status = self.translate_teuteu_error_status(self.get_state("vacuum.teuteu" , attribute = "status"))
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "⚠️ TeuTeu est en erreur", 
        message = status,
        image_url = current_location,
        click_url = "/lovelace/teuteu",
        icon =  "mdi:robot-vacuum-variant",
        color = "#ff6e07")

  """
  Callback triggered when is not on the dock since more than 30 mintues
  Goals : 
  . Notify
  """ 
  def callback_teuteu_idle(self, entity, attribute, old, new, kwargs):
    if old != new:
      self.log("Detecting that teuteu is not plugged since more than 30 miuntes. Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_to_present",
        title = "️🪫 TeuTeu se décharge",
        message = "Je detecte que TeuTeu n'est plus sur sa base depuis plus de 30 minutes",
        click_url="/lovelace/teuteu",
        icon =  "mdi:robot-vacuum-variant",
        color = "#ff6e07")


  """
  Callback triggered when button "cancel_planned_teuteu" is clicked from a notification
  Goals :
  . Cancel planned cleaning
  """
  def callback_button_clicked_cancel_planned_teuteu(self, event_name, data, kwargs):
    self.log("Notification button clicked : canceling scheduled cleaning") 
    self.log("House cleaning canceled")
    # Cancel cleaning
    self.cancel_timer(self.cleaning_handle)

  """
  Callback triggered when button "cancel_planned_teuteu_and_start_now" is clicked from a notification
  Goals :
  . Cancel planned cleaning
  . Clean now
  """
  def callback_button_clicked_cancel_planned_teuteu_and_start_now(self, event_name, data, kwargs):
    self.log("Notification button clicked : canceling scheduled cleaning and starting cleaning now") 
    # Cancel cleaning
    self.cancel_timer(self.cleaning_handle)
    self.log("House cleaning will start now")
    # Start TeuTeu
    self.call_service("vacuum/start" , entity_id = "vacuum.teuteu")


  """
  Callback triggered when button "rth_teuteu" is clicked from a notification
  Goals :
  . RTH TeuTeu
  """
  def callback_button_clicked_rth_teuteu(self, event_name, data, kwargs):
    self.log("Notification button clicked : RTH Spirro") 
    self.call_service("vacuum/return_to_base" , entity_id = "vacuum.teuteu")

  """
  Helper method:
  Does : 
  . Translate known English status in French
  Returns : the translated status

  """
  def translate_teuteu_error_status(self, status):
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
    
