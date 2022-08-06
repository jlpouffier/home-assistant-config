import hassapi as hass
import datetime

"""
clean_house is an app responsible of the scheduling of TeuTeu and NeuNeu

Functionalities :
. Starts TeuTeu when needed

Notifications :
. Cleaning Started > RTH possible
. Cleaning Finished
. TeuTeu error
. TeuTeu not on the dock
"""
class clean_house(hass.Hass):
  def initialize(self):
    self.listen_state(self.callback_home_empty, "binary_sensor.home_occupied", new= "off", immediate = True)
    self.listen_state(self.callback_first_floor_dirty, "binary_sensor.should_teuteu_run" , new = "on", immediate = True)
    
    self.listen_state(self.callback_teuteu_started, "vacuum.teuteu" , old = "docked" , new = "cleaning")
    self.listen_state(self.callback_teuteu_cleaning_for_more_than_x_minutes, "vacuum.teuteu" , new = "cleaning", duration = 900)
    self.listen_state(self.callback_teuteu_finished, "vacuum.teuteu",  new = "docked")
    self.listen_state(self.callback_teuteu_error, "vacuum.teuteu" , new = "error", immediate = True)
    self.listen_state(self.callback_teuteu_idle, "vacuum.teuteu" , new = "idle" , duration = 1800)
    
    #Listen to button press from notification
    self.listen_event(self.callback_button_clicked_rth_teuteu, "mobile_app_notification_action", action = "rth_teuteu")

    self.log("House cleaning Automation initialized")

  """
  Callback triggered when the home is empty
  Goals :
  . Check if home dirtly
  . Check if we are not cleaning right now
  . If all 2 conditions are met:
    . Start cleaning
  """ 
  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    self.log("Home empty, Checking if TeuTeu can run now ... ")
    # Is First floor dirty
    is_first_floor_dirty = True if self.get_state("binary_sensor.should_teuteu_run") == "on" else False
    # Are we cleaning right now ?
    is_teuteu_cleaning_right_now = True if self.get_state("vacuum.teuteu") == "cleaning" else False

    if is_first_floor_dirty  and not is_teuteu_cleaning_right_now:
      self.log("TeuTeu will start cleaning now ...")
      self.call_service("vacuum/start" , entity_id = "vacuum.teuteu")

  """
  Callback triggered when the home is dirty
  Goals :
  . Check if home empty
  . Check if we are not cleaning right now
  . If all 2 conditions are met:
    . Start cleaning
  """ 
  def callback_first_floor_dirty(self, entity, attribute, old, new, kwargs):
    self.log("First floor dirtly now ... Checking if TeuTeu can run now ...  ")
    # Are we cleaning right now ?
    is_teuteu_cleaning_right_now = True if self.get_state("vacuum.teuteu") == "cleaning" else False
    # Is home occupied ?
    is_home_empty = True if self.get_state("binary_sensor.home_occupied") == "off" else False

    if is_home_empty and not is_teuteu_cleaning_right_now:
      self.log("TeuTeu will start cleaning now ...")
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
    
