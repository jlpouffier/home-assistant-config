import hassapi as hass

"""
monitor_home is an app responsible of the monitoring the home 

Functionalities :
. Turn off Alexa if the home is not occupied

Notifications :
. Home empty and Lights on > Turn off possible
. Home empty and TV on > Turn off possible
. Home empty and LSX still on > Turn off possible
. Home empty and coffee maker on > Turn off possible
. Home empty and doors / window still opened
. Home occupied and doors / window still open (As a reminder)
. Raining and doors / windows open
. Coffe maker on for more than 90 minutes > Turn off possible

"""
class monitor_home(hass.Hass): 
  def initialize(self):
    self.listen_state(self.callback_home_empty , "binary_sensor.home_occupied" , old = "on" , new = "off")
    self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" , old = "off" , new = "on")
    self.listen_state(self.callback_coffee_maker_on_since_too_long , "switch.coffeemaker" , new = "on", duration = 5400)
    self.listen_state(self.callback_raining_now, "binary_sensor.is_raining_now", new = "on")

    self.listen_event(self.callback_button_clicked_turn_off_lights, "mobile_app_notification_action", action = "turn_off_lights")
    self.listen_event(self.callback_button_clicked_turn_off_tv, "mobile_app_notification_action", action = "turn_off_tv")
    self.listen_event(self.callback_button_clicked_turn_off_lsx, "mobile_app_notification_action", action = "turn_off_lsx")
    self.listen_event(self.callback_button_clicked_turn_off_coffee_maker, "mobile_app_notification_action", action = "turn_off_coffee_maker")
    
  """
  Callback triggered when the home becomes not occupied
  Goals :
  . Turn off Alexa
  . Send notification(s)
  """
  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    self.log("Detecting home empty ...")

    # turning off Alexa
    self.log("... Turning off Alexa.")
    self.call_service("switch/turn_off", entity_id = "switch.alexa")

    # test if lights are still on
    if self.entities.light.all_lights.state == "on":
      self.log("... Lights on. Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "💡 Lumières allumées", 
        message = "Des lumières sont allumées alors que personne n'est présent",
        callback = [{
          "title" : "Éteindre les lumières",
          "event" : "turn_off_lights"}],
        click_url="/lovelace/lights",
        icon =  "mdi:lightbulb-alert",
        color = "#ff6e07",
        tag = "home_empty_lights_still_on",
        until =  [{
          "entity_id" : "binary_sensor.home_occupied",
          "new_state" : "on"},{
          "entity_id" : "light.all_lights",
          "new_state" : "off"}])

    # test if TV is still on
    if self.entities.binary_sensor.is_tv_on.state == "on":
      self.log("... TV on. Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "📺 TV allumée", 
        message = "La TV est allumée alors que personne n'est présent",
        callback = [{
          "title" : "Éteindre la TV",
          "event" : "turn_off_tv"}],
        click_url="/lovelace/connected-devices",
        icon =  "mdi:television",
        color = "#ff6e07",
        tag = "home_empty_tv_still_on",
        until =  [{
          "entity_id" : "binary_sensor.home_occupied",
          "new_state" : "on"},{
          "entity_id" : "binary_sensor.is_tv_on",
          "new_state" : "off"}])

    # test if LSX is still on
    if self.entities.media_player.kef.state == "on":
      self.log("... LSX on. Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "🔊 LSX allumées", 
        message = "Les enceintes LSX sont allumées alors que personne n'est présent",
        callback = [{
          "title" : "Éteindre les LSX",
          "event" : "turn_off_lsx"}],
        click_url="/lovelace/connected-devices",
        icon =  "mdi:speaker-wireless",
        color = "#ff6e07",
        tag = "home_empty_lsx_still_on",
        until =  [{
          "entity_id" : "binary_sensor.home_occupied",
          "new_state" : "on"},{
          "entity_id" : "media_player.kef",
          "new_state" : "off"}])

    # test is coffe maker still on
    if self.entities.switch.coffeemaker.state == "on":
      self.log("... Coffee maker on. Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "️☕️ Machine a café allumé", 
        message = "La machine a café est allumée alors que personne n'est présent",
        callback = [{
          "title" : "Éteindre la machine a café",
          "event" : "turn_off_coffee_maker"}],
        click_url="/lovelace/connected-devices",
        icon =  "mdi:coffee",
        color = "#ff6e07",
        tag = "home_empty_cofee_maker_still_on",
        until =  [{
          "entity_id" : "binary_sensor.home_occupied",
          "new_state" : "on"},{
          "entity_id" : "switch.coffeemaker",
          "new_state" : "off"}])

    # test if doors are still open
    if self.entities.binary_sensor.all_doors.state == "on":
      self.log("... some doors are still opened. notifying it")
      doors = self.entities.binary_sensor.all_doors.attributes.entity_id
      open_doors = []
      for door in doors:
        if self.get_state(door) == "on":
          friendly_name_door = self.get_state(door, attribute = "friendly_name")
          open_doors.append(friendly_name_door)
      if len(open_doors) == 1:
        self.fire_event("NOTIFIER",
          action = "send_to_nearest",
          title = "️🚪 Porte ouverte !", 
          message = "La " + open_doors[0] + " est toujours ouverte alors que personne n'est présent !",
          click_url="/lovelace/openings",
          icon =  "mdi:door-open",
          color = "#ff6e07",
          tag = "home_empty_door_open",
          until =  [{
            "entity_id" : "binary_sensor.home_occupied",
            "new_state" : "on"},{
            "entity_id" : "binary_sensor.all_doors",
            "new_state" : "off"}])
      elif len(open_doors) > 1:
        self.fire_event("NOTIFIER",
          action = "send_to_nearest",
          title = "️🚪 Porte ouverte !", 
          message = "Les portes suivantes sont toujours ouvertes alors que personne n'est présent: " + ", ".join(open_doors),
          click_url="/lovelace/openings",
          icon =  "mdi:door-open",
          color = "#ff6e07",
          tag = "home_empty_door_open",
          until =  [{
            "entity_id" : "binary_sensor.home_occupied",
            "new_state" : "on"},{
            "entity_id" : "binary_sensor.all_doors",
            "new_state" : "off"}])

    # test if windows are still open
    if self.entities.binary_sensor.all_windows.state == "on":
      self.log("... some windows are still opened. notifying it")
      windows = self.entities.binary_sensor.all_windows.attributes.entity_id
      open_windows = []
      for window in windows:
        if self.get_state(window) == "on":
          friendly_name_window = self.get_state(window, attribute = "friendly_name")
          open_windows.append(friendly_name_window)
      if len(open_windows) == 1:
        self.fire_event("NOTIFIER",
          action = "send_to_nearest",
          title = "️🚪 Fenêtre ouverte !", 
          message = "La " + open_windows[0] + " est toujours ouverte alors que personne n'est présent !",
          click_url="/lovelace/openings",
          icon =  "mdi:window-open",
          color = "#ff6e07",
          tag = "home_empty_window_open",
          until =  [{
            "entity_id" : "binary_sensor.home_occupied",
            "new_state" : "on"},{
            "entity_id" : "binary_sensor.all_windows",
            "new_state" : "off"}])
      elif len(open_windows) > 1:
        self.fire_event("NOTIFIER",
          action = "send_to_nearest",
          title = "️🚪 Fenêtre ouverte !", 
          message = "Les fenêtres suivantes sont toujours ouvertes alors que personne n'est présent: " + ", ".join(open_windows),
          click_url="/lovelace/openings",
          icon =  "mdi:window-open",
          color = "#ff6e07",
          tag = "home_empty_window_open",
          until =  [{
            "entity_id" : "binary_sensor.home_occupied",
            "new_state" : "on"},{
            "entity_id" : "binary_sensor.all_windows",
            "new_state" : "off"}])

  """
  Callback triggered when the home becomes occupied
  Goals :
  . Turn on Alexa
  . Remind occupant if doors / windos are still open.
  """
  def callback_home_occupied(self, entity, attribute, old, new, kwargs):
    self.log("Detecting home occupied...")

    # turn on alexa
    self.log("... Turning on Alexa.")
    self.call_service("switch/turn_on", entity_id = "switch.alexa")

    # test if doors are still open and send reminder if it's the case
    if self.entities.binary_sensor.all_doors.state == "on":
      self.log("... some doors are still opened. notifying it")
      doors = self.entities.binary_sensor.all_doors.attributes.entity_id
      open_doors = []
      for door in doors:
        if self.get_state(door) == "on":
          friendly_name_door = self.get_state(door, attribute = "friendly_name")
          open_doors.append(friendly_name_door)
      if len(open_doors) == 1:
        self.fire_event("NOTIFIER",
          action = "send_to_present",
          title = "️🚪 Porte ouverte !", 
          message = "Rappel: La " + open_doors[0] + " est toujours ouverte",
          click_url="/lovelace/openings",
          icon =  "mdi:door-open",
          color = "#ff6e07",
          tag = "home_occupied_door_open",
          until =  [{
            "entity_id" : "binary_sensor.all_doors",
            "new_state" : "off"}])
      elif len(open_doors) > 1:
        self.fire_event("NOTIFIER",
          action = "send_to_present",
          title = "️🚪 Porte ouverte !", 
          message = "Rappel: Les portes suivantes sont toujours ouvertes: " + ", ".join(open_doors),
          click_url="/lovelace/openings",
          icon =  "mdi:door-open",
          color = "#ff6e07",
          tag = "home_occupied_door_open",
          until =  [{
            "entity_id" : "binary_sensor.all_doors",
            "new_state" : "off"}])

    # test if windows are still open
    if self.entities.binary_sensor.all_windows.state == "on":
      self.log("... some windows are still opened. notifying it")
      windows = self.entities.binary_sensor.all_windows.attributes.entity_id
      open_windows = []
      for window in windows:
        if self.get_state(window) == "on":
          friendly_name_window = self.get_state(window, attribute = "friendly_name")
          open_windows.append(friendly_name_window)
      if len(open_windows) == 1:
        self.fire_event("NOTIFIER",
          action = "send_to_present",
          title = "️🚪 Fenêtre ouverte !", 
          message = "Rappel: La " + open_windows[0] + " est toujours ouverte",
          click_url="/lovelace/openings",
          icon =  "mdi:window-open",
          color = "#ff6e07",
          tag = "home_occupied_window_open",
          until =  [{
            "entity_id" : "binary_sensor.all_windows",
            "new_state" : "off"}])
      elif len(open_windows) > 1:
        self.fire_event("NOTIFIER",
          action = "send_to_present",
          title = "️🚪 Fenêtre ouverte !", 
          message = "Rappel: Les fenêtres suivantes sont toujours ouvertes: " + ", ".join(open_windows),
          click_url="/lovelace/openings",
          icon =  "mdi:window-open",
          color = "#ff6e07",
          tag = "home_occupied_window_open",
          until =  [{
            "entity_id" : "binary_sensor.all_windows",
            "new_state" : "off"}])

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
        click_url="/lovelace/connected-devices",
        icon = "mdi:coffee",
        color = "#ff6e07",
        tag = "coffee_maker_on_since_too_long",
        until =  [{
          "entity_id" : "switch.coffeemaker",
          "new_state" : "off"}])

  """
  Callback triggered when it starts to rain
  Goals :
  . Notify present occupants if doors are open.
  """
  def callback_raining_now(self, entity, attribute, old, new, kwargs):
    if self.entities.binary_sensor.home_occupied.state == "on" and self.entities.binary_sensor.all_openings.state == "on":
      self.log("It is raining now, the hoome is occupied and some openings are open: Notifying it...")

      # test if doors are still open
      if self.entities.binary_sensor.all_doors.state == "on":
        doors = self.entities.binary_sensor.all_doors.attributes.entity_id
        open_doors = []
        for door in doors:
          if self.get_state(door) == "on":
            friendly_name_door = self.get_state(door, attribute = "friendly_name")
            open_doors.append(friendly_name_door)
        if len(open_doors) == 1:
          self.fire_event("NOTIFIER",
            action = "send_to_present",
            title = "️🌂 Il pleut!", 
            message = "La " + open_doors[0] + " est ouverte et il commence a pleuvoir !",
            click_url="/lovelace/openings",
            icon =  "mdi:door-open",
            color = "#ff6e07",
            tag = "raining_door_open",
            until =  [{
              "entity_id" : "binary_sensor.is_raining_now",
              "new_state" : "off"},{
              "entity_id" : "binary_sensor.all_doors",
              "new_state" : "off"}])
        elif len(open_doors) > 1:
          self.fire_event("NOTIFIER",
            action = "send_to_present",
            title = "️🌂 Il pleut!", 
            message = "Les portes suivantes sont ouvertes et il commence a pleuvoir: " + ", ".join(open_doors),
            click_url="/lovelace/openings",
            icon =  "mdi:door-open",
            color = "#ff6e07",
            tag = "raining_door_open",
            until =  [{
              "entity_id" : "binary_sensor.is_raining_now",
              "new_state" : "off"},{
              "entity_id" : "binary_sensor.all_doors",
              "new_state" : "off"}])

      # test if windows are still open
      if self.entities.binary_sensor.all_windows.state == "on":
        self.log("... some windows are still opened. notifying it")
        windows = self.entities.binary_sensor.all_windows.attributes.entity_id
        open_windows = []
        for window in windows:
          if self.get_state(window) == "on":
            friendly_name_window = self.get_state(window, attribute = "friendly_name")
            open_windows.append(friendly_name_window)
        if len(open_windows) == 1:
          self.fire_event("NOTIFIER",
            action = "send_to_present",
            title = "️🌂 Il pleut!", 
            message = "La " + open_windows[0] + " est ouverte  et il commence a pleuvoir !",
            click_url="/lovelace/openings",
            icon =  "mdi:window-open",
            color = "#ff6e07",
            tag = "raining_window_open",
            until =  [{
              "entity_id" : "binary_sensor.is_raining_now",
              "new_state" : "off"},{
              "entity_id" : "binary_sensor.all_windows",
              "new_state" : "off"}])
        elif len(open_windows) > 1:
          self.fire_event("NOTIFIER",
            action = "send_to_present",
            title = "️🌂 Il pleut!", 
            message = "Les fenêtres suivantes sont ouvertes et il commence a pleuvoir: " + ", ".join(open_windows),
            click_url="/lovelace/openings",
            icon =  "mdi:window-open",
            color = "#ff6e07",
            tag = "raining_window_open",
            until =  [{
              "entity_id" : "binary_sensor.is_raining_now",
              "new_state" : "off"},{
              "entity_id" : "binary_sensor.all_windows",
              "new_state" : "off"}])

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
  Callback triggered when button "turn_off_lsx" is clicked from a notification
  Goals :
  . Turn off LSX
  """
  def callback_button_clicked_turn_off_lsx(self, event_name, data, kwargs):
    self.log("Notification button clicked : Turning off LSX") 
    self.call_service("media_player/turn_off" , entity_id = "media_player.kef")


  """
  Callback triggered when button "turn_off_coffee_maker" is clicked from a notification
  Goals :
  . Turn off coffee maker
  """
  def callback_button_clicked_turn_off_coffee_maker(self, event_name, data, kwargs):
    self.log("Notification button clicked : Turning off coffee maker")
    self.call_service("switch/turn_off" , entity_id = "switch.coffeemaker")