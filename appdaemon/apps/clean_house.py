import hassapi as hass

"""
clean_house is an app responsible of the scheduling of TeuTeu and NeuNeu

Functionalities :
  Starts TeuTeu when needed
  Starts NeuNeu when needed

Notifications :
  Cleaning Started > RTH possible
  Cleaning Finished
  Vacuum error
  Vacuum not on the dock
"""
class clean_house(hass.Hass):
  def initialize(self):
    # Minimum Cleaning Duration. 
    self.minimum_cleaning_duration = 15 * 60

    self.listen_state(self.callback_home_empty, "binary_sensor.home_occupied", new= "off", immediate = True)
    self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" , old = "off" , new = "on")
    self.listen_state(self.callback_first_floor_dirty, "binary_sensor.should_neuneu_run" , new = "on", immediate = True)
    self.listen_state(self.callback_first_floor_very_dirty, "binary_sensor.should_neuneu_run_urgently" , new = "on", immediate = True)
    self.listen_state(self.callback_second_floor_dirty, "binary_sensor.should_teuteu_run" , new = "on", immediate = True)
    self.listen_state(self.callback_second_floor_very_dirty, "binary_sensor.should_teuteu_run_urgently" , new = "on", immediate = True)
    
    # Shared callbacks between TeuTeu and NeuNeu
    self.listen_state(self.callback_vacuum_started, "vacuum" , new = "cleaning")
    self.listen_state(self.callback_vacuum_finished, "vacuum",  new = "docked")
    self.listen_state(self.callback_vacuum_error, "vacuum" , new = "error", immediate = True)

    # TEUTEU CALLBACKS
    self.listen_state(self.callback_vacuum_cleaning_for_more_than_x_minutes, "vacuum.teuteu" , new = "cleaning", duration = self.minimum_cleaning_duration)
    self.listen_state(self.callback_teuteu_idle, "vacuum.teuteu" , new = "idle" , duration = 1800)

    # NEUNEU CALLBACKS
    self.listen_state(self.callback_vacuum_cleaning_for_more_than_x_minutes, "vacuum.neuneu" , new = "cleaning", duration = self.minimum_cleaning_duration)

    #Listen to button press from notification
    self.listen_event(self.callback_button_clicked_rth_teuteu, "mobile_app_notification_action", action = "rth_teuteu")
    self.listen_event(self.callback_button_clicked_start_teuteu, "mobile_app_notification_action", action = "start_teuteu")
    self.listen_event(self.callback_button_clicked_rth_neuneu, "mobile_app_notification_action", action = "rth_neuneu")
    self.listen_event(self.callback_button_clicked_start_neuneu, "mobile_app_notification_action", action = "start_neuneu")
  
  """
  Callback triggered when the home is empty
  Goals :
    Check if home dirtly
    Check if we are not cleaning right now
    If all 2 conditions are met:
      Start cleaning
  """ 
  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    self.log("Home empty, Checking if vacuums can run now ... ")
    # Is first floor dirty
    is_first_floor_dirty = True if self.entities.binary_sensor.should_neuneu_run.state == "on" else False

    # Is second floor dirty
    is_second_floor_dirty = True if self.entities.binary_sensor.should_teuteu_run.state == "on" else False

    # Is first floor in scope ?
    is_first_floor_in_scope = True if self.entities.input_boolean.house_cleaning_first_floor.state == "on" else False

    # Is second floor in scope ?
    is_second_floor_in_scope = True if self.entities.input_boolean.house_cleaning_second_floor.state == "on" else False

    # Is teuteu cleaning now ?
    is_teuteu_cleaning_right_now = True if self.entities.vacuum.teuteu.state == "cleaning" else False
    
    # Is neuneu cleaning now ?
    is_neuneu_cleaning_right_now = True if self.entities.vacuum.neuneu.state == "cleaning" else False


    if is_second_floor_dirty and is_second_floor_in_scope and not is_teuteu_cleaning_right_now:
      self.log("TeuTeu will start cleaning now ...")
      #self.call_service("vacuum/start" , entity_id = "vacuum.teuteu")
      self.call_service("neato/custom_cleaning" , entity_id = "vacuum.teuteu" , mode = 1 , navigation = 2 , category = 2)
    
    if is_first_floor_dirty and is_first_floor_in_scope and not is_neuneu_cleaning_right_now:
      self.log("NeuNeu will start cleaning now ...")
      self.call_service("vacuum/start" , entity_id = "vacuum.neuneu")
    
  """
  Callback triggered when the home is occupied
  Goals :
    RTH vacuums
  """ 
  def callback_home_occupied(self, entity, attribute, old, new, kwargs):
    self.log("Home occupied, Checking if vacuums should stop now ... ")
    if self.entities.vacuum.teuteu.state == 'cleaning':
      # Stopping TeuTeu
      self.log("RTH TeuTeu") 
      self.call_service("vacuum/return_to_base" , entity_id = "vacuum.teuteu")
    
    if self.entities.vacuum.neuneu.state == 'cleaning':
      # Stopping NeuNeu
      self.log("RTH NeuNeu") 
      self.call_service("vacuum/return_to_base" , entity_id = "vacuum.neuneu")

  """
  Callback triggered when the first floor is dirty
  Goals :
    Check if home empty
    Check if we are not cleaning right now
    If all 2 conditions are met:
      Start cleaning
  """ 
  def callback_first_floor_dirty(self, entity, attribute, old, new, kwargs):
    self.log("First floor dirtly now ... Checking if NeuNeu can run now ...  ")
    # Are we cleaning right now ?
    is_neuneu_cleaning_right_now = True if self.entities.vacuum.neuneu.state == "cleaning" else False
    # Is home occupied ?
    is_home_empty = True if self.entities.binary_sensor.home_occupied.state == "off" else False
    # Is first floor in scope ?
    is_first_floor_in_scope = True if self.entities.input_boolean.house_cleaning_first_floor.state == "on" else False

    if is_home_empty and is_first_floor_in_scope and not is_neuneu_cleaning_right_now:
      self.log("NeuNeu will start cleaning now ...")
      self.call_service("vacuum/start" , entity_id = "vacuum.neuneu")

  """
  Callback triggered when the fisrt floor is very dirty
  Goals :
    Notify
  """ 
  def callback_first_floor_very_dirty(self, entity, attribute, old, new, kwargs):
    if self.entities.input_boolean.house_cleaning_first_floor.state == "on":
      self.log("First floor super dirtly now ... Notifying it.  ")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "🧹 Rez-de-chaussé sale", 
        message = "NeuNeu n'a pas tourné depuis longtemps! Ne pas oublier de le lancer!",
        callback = [{
          "title" : "Lancer NeuNeu",
          "event" : "start_neuneu"}],
        click_url="/lovelace/vacuums",
        icon = "mdi:liquid-spot",
        color = "deep-orange",
        tag = "first_floor_very_dirty",
        until =  [{
          "entity_id" : "vacuum.neuneu",
          "new_state" : "cleaning"}])

  """
  Callback triggered when the second floor is dirty
  Goals :
    Check if home empty
    Check if we are not cleaning right now
    If all 2 conditions are met:
      Start cleaning
  """ 
  def callback_second_floor_dirty(self, entity, attribute, old, new, kwargs):
    self.log("Second floor dirtly now ... Checking if TeuTeu can run now ...  ")
    # Are we cleaning right now ?
    is_teuteu_cleaning_right_now = True if self.entities.vacuum.teuteu.state == "cleaning" else False
    # Is home occupied ?
    is_home_empty = True if self.entities.binary_sensor.home_occupied.state == "off" else False
    # Is second floor in scope ?
    is_second_floor_in_scope = True if self.entities.input_boolean.house_cleaning_second_floor.state == "on" else False

    if is_home_empty and is_second_floor_in_scope and not is_teuteu_cleaning_right_now:
      self.log("TeuTeu will start cleaning now ...")
      #self.call_service("vacuum/start" , entity_id = "vacuum.teuteu")
      self.call_service("neato/custom_cleaning" , entity_id = "vacuum.teuteu" , mode = 1 , navigation = 2 , category = 2)

  """
  Callback triggered when the second floor is very dirty
  Goals :
    Notify
  """ 
  def callback_second_floor_very_dirty(self, entity, attribute, old, new, kwargs):
    if self.entities.input_boolean.house_cleaning_second_floor.state == "on":
      self.log("Second floor super dirtly now ... Notifying it.  ")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "🧹 Premier étage sale", 
        message = "TeuTeu n'a pas tourné depuis longtemps! Ne pas oublier de le lancer!",
        callback = [{
          "title" : "Lancer TeuTeu",
          "event" : "start_teuteu"}],
        click_url="/lovelace/vacuums",
        icon = "mdi:liquid-spot",
        color = "deep-orange",
        tag = "second_floor_very_dirty",
        until =  [{
          "entity_id" : "vacuum.teuteu",
          "new_state" : "cleaning"}])

  """
  Callback triggered when a vacuum is starting
  Goals : 
    Notify
  """   
  def callback_vacuum_started(self, entity, attribute, old, new, kwargs):
    if entity == "vacuum.teuteu":
      event = "rth_teuteu"
      vacuum_name = "TeuTeu"
      icon = "mdi:robot-vacuum-variant"

    if entity == "vacuum.neuneu":
      event = "rth_neuneu"
      vacuum_name = "NeuNeu"
      icon = "mdi:robot-vacuum"

    self.log("Detecting that a vacuum is starting. Notifying it...")
    self.fire_event("NOTIFIER",
      action = "send_to_nearest",
      title = "🧹 Nettoyage", 
      message = vacuum_name + " démarre son nettoyage",
      callback = [{
        "title" : "Arrêter " + vacuum_name,
        "event" : event}],
      click_url="/lovelace/vacuums",
      icon = icon,
      tag = vacuum_name.lower())



  """
  Callback triggered when a vacuum is cleaning for more than 15 minutes
  Goals : 
    Update input_datetime.dernier_nettoyage_de_teuteu or input_datetime.dernier_nettoyage_de_neuneu
  """   
  def callback_vacuum_cleaning_for_more_than_x_minutes(self, entity, attribute, old, new, kwargs):
    self.log("A vacuum is cleaning since more than 15 minutes, updating the last clean-up datetime...")

    if entity == "vacuum.teuteu":
      self.call_service("input_datetime/set_datetime", entity_id = "input_datetime.dernier_nettoyage_de_teuteu", timestamp = self.get_now_ts())
    
    if entity == "vacuum.neuneu":
      self.call_service("input_datetime/set_datetime", entity_id = "input_datetime.dernier_nettoyage_de_neuneu", timestamp = self.get_now_ts())


  """
  Callback triggered when a vacuum is finished
  Goals : 
    Notify
  """ 
  def callback_vacuum_finished(self, entity, attribute, old, new, kwargs):
    if old in ["paused", "cleaning", "returning"]: 
      self.log("Detecting that a vacuum has finished. Notifying it...")

      if entity == "vacuum.teuteu":
        area_cleaned = self.entities.sensor.teuteu_last_cleaning_area.state
        cleaned_map = self.args["hass_base_url"] + self.entities.camera.teuteu_cleaning_map.attributes.entity_picture
        vacuum_name = "TeuTeu"
        icon = "mdi:robot-vacuum-variant"
      
      if entity == "vacuum.neuneu":
        area_cleaned = self.entities.sensor.neuneu_cleaned_area.state
        cleaned_map = self.args["hass_base_url"] + self.entities.camera.neuneu_map.attributes.entity_picture
        vacuum_name = "NeuNeu"
        icon = "mdi:robot-vacuum"
      
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "✅ " + vacuum_name + " a terminé",
        message = "Surface nettoyée: " + area_cleaned + "m2",
        image_url = cleaned_map,
        click_url="/lovelace/vacuums",
        icon =  icon,
        color = "green",
        tag = vacuum_name.lower())
      
      if entity == "vacuum.neuneu" and self.entities.sensor.neuneu_water_tank.state == "installed":
        self.log("Water tank still installed to NeuNeu. Notifying it...")
        self.fire_event("NOTIFIER",
          action = "send_when_present",
          title = "🧼 Serpillière attachée",
          message = "La serpillière est toujours attachée à NeuNeu. Pensez a l'enlever!",
          click_url="/lovelace/vacuums",
          icon =  "mdi:faucet",
          color = "deep-orange",
          tag = "neuneu_mop_installed",
          until =  [{
            "entity_id" : "sensor.neuneu_water_tank",
            "new_state" : "not_installed"}])

  """
  Callback triggered when teuteu is in error
  Goals : 
    Notify
  """ 
  def callback_vacuum_error(self, entity, attribute, old, new, kwargs):
    self.log("Detecting that a vacuum is in trouble. Notifying it...")

    if entity == "vacuum.teuteu":
      current_location = self.args["hass_base_url"] + self.entities.camera.teuteu_cleaning_map.attributes.entity_picture
      status = self.translate_teuteu_error_status(self.entities.vacuum.teuteu.attributes.status)
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "⚠️ TeuTeu est en erreur", 
        message = status,
        image_url = current_location,
        click_url = "/lovelace/vacuums",
        icon =  "mdi:robot-vacuum-variant",
        color = "deep-orange",
        tag = "teuteu")
    
    if entity == "vacuum.neuneu":
      # TO EXPLORE ONCE NEUNEU STARTS RAISING ERRORS
      current_location = self.args["hass_base_url"] + self.entities.camera.neuneu_map.attributes.entity_picture
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        message = "NeuNeu est en erreur",
        title = "⚠️ NeuNeu est en erreur", 
        image_url = current_location,
        click_url = "/lovelace/vacuums",
        icon =  "mdi:robot-vacuum",
        color = "deep-orange",
        tag = "neuneu")

  """
  Callback triggered when is not on the dock since more than 30 mintues
  Goals : 
    Notify
  """ 
  def callback_teuteu_idle(self, entity, attribute, old, new, kwargs):
    if old != new:
      self.log("Detecting that teuteu is not plugged since more than 30 miuntes. Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_to_present",
        title = "️🪫 TeuTeu se décharge",
        message = "Je detecte que TeuTeu n'est plus sur sa base depuis plus de 30 minutes",
        click_url="/lovelace/vacuums",
        icon =  "mdi:robot-vacuum-variant",
        color = "deep-orange",
        tag = "teuteu",
        until =  [{
          "entity_id" : "vacuum.teuteu",
          "new_state" : "docked"}])

  """
  Callback triggered when button "rth_teuteu" is clicked from a notification
  Goals :
    RTH TeuTeu
  """
  def callback_button_clicked_rth_teuteu(self, event_name, data, kwargs):
    self.log("Notification button clicked : RTH TeuTeu") 
    # RTH TeuTeu
    self.call_service("vacuum/return_to_base" , entity_id = "vacuum.teuteu")

  """
  Callback triggered when button "start_teuteu" is clicked from a notification
  Goals :
    Start TeuTeu
  """
  def callback_button_clicked_start_teuteu(self, event_name, data, kwargs):
    self.log("Notification button clicked : Start TeuTeu") 
    #self.call_service("vacuum/start" , entity_id = "vacuum.teuteu")
    self.call_service("neato/custom_cleaning" , entity_id = "vacuum.teuteu" , mode = 1 , navigation = 2 , category = 2)

  """
  Callback triggered when button "rth_neuneu" is clicked from a notification
  Goals :
    RTH NeuNeu
  """
  def callback_button_clicked_rth_neuneu(self, event_name, data, kwargs):
    self.log("Notification button clicked : RTH neuneu") 

    # RTH neuneu
    self.call_service("vacuum/return_to_base" , entity_id = "vacuum.neuneu")

  """
  Callback triggered when button "start_neuneu" is clicked from a notification
  Goals :
    Start NeuNeu
  """
  def callback_button_clicked_start_neuneu(self, event_name, data, kwargs):
    self.log("Notification button clicked : Start neuneu") 
    self.call_service("vacuum/start" , entity_id = "vacuum.neuneu")
  
  """
  Helper method:
  Does : 
    Translate known English status in French
  Returns : 
    The translated status
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