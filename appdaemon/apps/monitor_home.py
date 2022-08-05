import hassapi as hass

"""
monitor_home is an app responsible of the monitoring the home 

Functionalities :
. RTH Spirro if home becomes occupied
. Stop presence simulator if home becomes occupied

Notifications :
. Home empty and Lights on > Turn off possible
. Home empty and TV on > Turn off possible
. Home empty and coffee maker on > Turn off possible
. Home empty and doors / window still opened
. Coffe maker on for more than 90 minutes > Turn off possible
. Washing Machine over

"""
class monitor_home(hass.Hass): 
  def initialize(self):
    self.listen_state(self.callback_home_empty , "binary_sensor.home_occupied" , old = "on" , new = "off")
    self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" , old = "off" , new = "on")
    self.listen_state(self.callback_coffee_maker_on_since_too_long , "switch.coffeemaker" , new = "on", duration = 5400)
    self.listen_state(self.callback_washing_mashine_over, "binary_sensor.is_washing_machine_running" , old = "on", new = "off")
    
    self.listen_event(self.callback_button_clicked_turn_off_lights, "mobile_app_notification_action", action = "turn_off_lights")
    self.listen_event(self.callback_button_clicked_turn_off_tv, "mobile_app_notification_action", action = "turn_off_tv")
    self.listen_event(self.callback_button_clicked_turn_off_coffee_maker, "mobile_app_notification_action", action = "turn_off_coffee_maker")
    
    self.log("Monitor Home initialized")
    
  """
  Callback triggered when the home becomes not occupied
  Goals :
  . Send notification(s)
  """
  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    self.log("Detecting home empty ...")
    # test if lights are still on
    if self.get_state("light.all_lights") == "on":
      self.log("... Lights on. Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "💡 Lumières allumées", 
        message = "Des lumières sont allumées alors que personne n'est présent",
        callback = [{
          "title" : "Éteindre les lumières",
          "event" : "turn_off_lights"}],
        click_url="/lovelace/apercu",
        icon =  "mdi:lightbulb-alert",
        color = "#ff6e07")

    # test if TV is still on
    if self.get_state("media_player.philips_android_tv") not in ["off", "standby", "unavailable"]:
      self.log("... TV on. Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "📺 TV allumée", 
        message = "La TV est allumée alors que personne n'est présent",
        callback = [{
          "title" : "Éteindre la TV",
          "event" : "turn_off_tv"}],
        click_url="/lovelace/day",
        icon =  "mdi:television",
        color = "#ff6e07")

    # test is coffe maker still on
    if self.get_state("switch.coffeemaker") == "on":
      self.log("... Coffee maker on. Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "️☕️ Machine a café allumé", 
        message = "La machine a café est allumée alors que personne n'est présent",
        callback = [{
          "title" : "Éteindre la machine a café",
          "event" : "turn_off_coffee_maker"}],
        click_url="/lovelace/day",
        icon =  "mdi:coffee",
        color = "#ff6e07")

    # test if doors or windows are still open
    if self.get_state("binary_sensor.all_doors") == "on":
      self.log("... some doors are still opened. notifying it")
      doors = self.get_state("binary_sensor.all_doors", attribute = "entity_id")
      for door in doors:
        if self.get_state(door) == "on":
          friendly_name_door = self.get_state(door, attribute = "friendly_name")
          self.fire_event("NOTIFIER",
            action = "send_to_nearest",
            title = "️🚪 Porte ouverte !", 
            message = "La " + friendly_name_door + " est toujours ouverte alors que personne n'est présent !",
            icon =  "mdi:door-open",
            color = "#ff6e07")
    
    if self.get_state("binary_sensor.all_windows") == "on":
      self.log("... some windows are still opened. notifying it")
      windows = self.get_state("binary_sensor.all_windows", attribute = "entity_id")
      for window in windows:
        if self.get_state(window) == "on":
          friendly_name_window = self.get_state(window, attribute = "friendly_name")
          self.fire_event("NOTIFIER",
            action = "send_to_nearest",
            title = "️🚪 Fenêtre ouverte !", 
            message = "La " + friendly_name_window + " est toujours ouverte alors que personne n'est présent !",
            icon =  "mdi:window-open",
            color = "#ff6e07")



  """
  Callback triggered when the home becomes occupied
  Goals :
  . Stop presence simulator (If turned on)
  . Stop Spiroo (if spirroo  on) 
  """
  def callback_home_occupied(self, entity, attribute, old, new, kwargs):
    self.log("Detecting home occupied...")
    if self.get_state("input_boolean.presence_simulator_switch") == "on":
      self.log("Stopping Presence Simulator")
      self.call_service("input_boolean/toggle", entity_id = "input_boolean.presence_simulator_switch")

    if self.get_state("vacuum.spiroo") == 'cleaning':
      # Stopping Spiroo
      self.log("RTH Spirro") 
      self.call_service("vacuum/return_to_base" , entity_id = "vacuum.spiroo")

  """
  Callback triggered when coffee maker on for more than 90 minutes
  Goals :
  . Send notification
  """
  def callback_coffee_maker_on_since_too_long(self, entity, attribute, old, new, kwargs):
    self.log("Detecting coffee maker on for more than 90 minutes. Notifying it...")
    self.fire_event("NOTIFIER",
        action = "send_to_present",
        title = "☕️ Machine a café allumé", 
        message = "La machine a café est allumée depuis longtemps",
        callback = [{
          "title" : "Éteindre la machine a café",
          "event" : "turn_off_coffee_maker"}],
        click_url="/lovelace/day",
        icon = "mdi:coffee",
        color = "#ff6e07")

  """
  Callback triggered when washing machine is over
  Goals :
  . Send notification
  """
  def callback_washing_mashine_over(self, entity, attribute, old, new, kwargs):
    self.log("Washing machine over. Notifying it...")
    self.fire_event("NOTIFIER",
        action = "send_when_present",
        title = "🫧 Machine à laver",
        message = "Cycle de lavage terminé !",
        icon =  "mdi:washing-machine",
        color = "#07ffc1")


  """
  Callback triggered when button "turn_off_lights" is clicked from a notification
  Goals :
  . Turn off all lights
  """
  def callback_button_clicked_turn_off_lights(self, event_name, data, kwargs):
    self.log("Notification button clicked : Turning off lights") 
    self.call_service("light/turn_off" , entity_id = "light.all_lights")

  """
  Callback triggered when button "turn_off_tv" is clicked from a notification
  Goals :
  . Turn off TV
  """
  def callback_button_clicked_turn_off_tv(self, event_name, data, kwargs):
    self.log("Notification button clicked : Turning off TV") 
    self.call_service("media_player/turn_off" , entity_id = "media_player.philips_android_tv")

  """
  Callback triggered when button "turn_off_coffee_maker" is clicked from a notification
  Goals :
  . Turn off coffee maker
  """
  def callback_button_clicked_turn_off_coffee_maker(self, event_name, data, kwargs):
    self.log("Notification button clicked : Turning off coffee maker")
    self.call_service("switch/turn_off" , entity_id = "switch.coffeemaker")
    