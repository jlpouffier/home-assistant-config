import hassapi as hass

"""
monitor_home is an app responsible of the monitoring the home 

Functionalities :
. Turn off Alexa if the home is not occupied
. Turn on and off lights, TV, KEF, coffee maker based on entry hue switch (long press)
. Deal with desynchronization edge case with my living room cover

Notifications :
. Home empty and Lights on > Turn off possible
. Home empty and TV on > Turn off possible
. Home empty and LSX still on > Turn off possible
. Home empty and coffee maker on > Turn off possible
. Home empty and doors / window still opened
. Coffe maker on for more than 90 minutes > Turn off possible
. Washing Machine over
. Mailbox full
. Cat Litter full > Cleaning possible
. Take out trash

"""
class monitor_home(hass.Hass): 
  def initialize(self):
    self.listen_state(self.callback_home_empty , "binary_sensor.home_occupied" , old = "on" , new = "off")
    self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" , old = "off" , new = "on")
    self.listen_state(self.callback_coffee_maker_on_since_too_long , "switch.coffeemaker" , new = "on", duration = 5400)
    self.listen_state(self.callback_washing_mashine_over, "binary_sensor.is_washing_machine_running" , old = "on", new = "off")
    self.listen_state(self.callback_mailbox_occupancy_detected, "binary_sensor.capteur_mouvement_boite_aux_lettres" , new = "on")
    self.listen_state(self.callback_litter_occupancy_detected, "binary_sensor.capteur_mouvement_litiere" , new = "on")
    self.listen_state(self.callback_litter_full, "binary_sensor.is_litter_full", new = "on")
    self.listen_state(self.callback_black_trash_schedule_begining, "schedule.planning_poubelle_noire", new = "on")
    self.listen_state(self.callback_green_trash_schedule_begining, "schedule.planning_poubelle_verte", new = "on")
    self.listen_state(self.callback_black_trash_schedule_end, "schedule.planning_poubelle_noire", new = "off")
    self.listen_state(self.callback_green_trash_schedule_end, "schedule.planning_poubelle_verte", new = "off")
    self.listen_event(self.callback_long_press_on_entry_switch_button_on, "hue_event", device_id = "64185ca2086c2ebd7b976a43ef0c89fd", unique_id = "c1c9f277-e27a-4340-9962-2206cc0d7e3a", type = "repeat", subtype = 1)
    self.listen_event(self.callback_long_press_on_entry_switch_button_off, "hue_event", device_id = "64185ca2086c2ebd7b976a43ef0c89fd", unique_id = "7564eab9-3cc9-4321-890c-1b9f1465f108", type = "repeat", subtype = 4)
    self.listen_event(self.callback_cover_open_service_called, "call_service", domain = "cover", service = "open_cover" , service_data = {"entity_id" : "cover.living_room_cover"})
    self.listen_event(self.callback_cover_close_service_called, "call_service", domain = "cover", service = "close_cover" , service_data = {"entity_id" : "cover.living_room_cover"})

    self.listen_event(self.callback_button_clicked_turn_off_lights, "mobile_app_notification_action", action = "turn_off_lights")
    self.listen_event(self.callback_button_clicked_turn_off_tv, "mobile_app_notification_action", action = "turn_off_tv")
    self.listen_event(self.callback_button_clicked_turn_off_lsx, "mobile_app_notification_action", action = "turn_off_lsx")
    self.listen_event(self.callback_button_clicked_turn_off_coffee_maker, "mobile_app_notification_action", action = "turn_off_coffee_maker")
    self.listen_event(self.callback_button_clicked_reset_litter_tracking, "mobile_app_notification_action", action = "reset_litter_tracking")

    
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
        color = "#ff6e07",
        tag = "home_empty_lights_still_on",
        until =  [{
          "entity_id" : "binary_sensor.home_occupied",
          "new_state" : "on"},{
          "entity_id" : "light.all_lights",
          "new_state" : "off"}])

    # test if TV is still on
    if self.get_state("binary_sensor.is_tv_on") == "on":
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
        color = "#ff6e07",
        tag = "home_empty_tv_still_on",
        until =  [{
          "entity_id" : "binary_sensor.home_occupied",
          "new_state" : "on"},{
          "entity_id" : "binary_sensor.is_tv_on",
          "new_state" : "off"}])

    # test if LSX is still on
    if self.get_state("media_player.kef") == "on":
      self.log("... LSX on. Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "🔊 LSX allumées", 
        message = "Les enceintes LSX sont allumées alors que personne n'est présent",
        callback = [{
          "title" : "Éteindre les LSX",
          "event" : "turn_off_lsx"}],
        click_url="/lovelace/day",
        icon =  "mdi:speaker-wireless",
        color = "#ff6e07",
        tag = "home_empty_lsx_still_on",
        until =  [{
          "entity_id" : "binary_sensor.home_occupied",
          "new_state" : "on"},{
          "entity_id" : "media_player.kef",
          "new_state" : "off"}])

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
        color = "#ff6e07",
        tag = "home_empty_cofee_maker_still_on",
        until =  [{
          "entity_id" : "binary_sensor.home_occupied",
          "new_state" : "on"},{
          "entity_id" : "switch.coffeemaker",
          "new_state" : "off"}])

    # test if doors are still open
    if self.get_state("binary_sensor.all_doors") == "on":
      self.log("... some doors are still opened. notifying it")
      doors = self.get_state("binary_sensor.all_doors", attribute = "entity_id")
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
          icon =  "mdi:door-open",
          color = "#ff6e07",
          tag = "home_empty_door_open",
          until =  [{
            "entity_id" : "binary_sensor.home_occupied",
            "new_state" : "on"},{
            "entity_id" : "binary_sensor.all_doors",
            "new_state" : "off"}])

    # test if windows are still open
    if self.get_state("binary_sensor.all_windows") == "on":
      self.log("... some windows are still opened. notifying it")
      windows = self.get_state("binary_sensor.all_windows", attribute = "entity_id")
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
  """
  def callback_home_occupied(self, entity, attribute, old, new, kwargs):
    self.log("Detecting home occupied... Turning on Alexa.")
    self.call_service("switch/turn_on", entity_id = "switch.alexa")

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
        color = "#ff6e07",
        tag = "coffee_maker_on_since_too_long",
        until =  [{
          "entity_id" : "switch.coffeemaker",
          "new_state" : "off"}])

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
      color = "#07ffc1",
      tag = "washing_mashine_over")


  """
  Callback triggered when mailbox occupancy is detected
  Goals :
  . Send notification, not when the main door is opened (rencently)
  . Discard notification when the main door is opened (rencently)
    (that's how I pick my mail)
  """
  def callback_mailbox_occupancy_detected(self, entity, attribute, old, new, kwargs):
    # if the main door was opened recently .. send notification
    if self.get_state("binary_sensor.is_front_door_recently_open") == "off":
      self.log("Occupancy detected in the mailbox + Door not opened recently: Notifying it...")
      self.fire_event("NOTIFIER",
        action = "send_when_present",
        title = "📬  Boite aux lettres",
        message = "Vous avez du courrier !",
        icon =  "mdi:mailbox-up",
        color = "#07ffc1",
        tag = "you_got_mail")
    # else discard
    else:
      self.log("Occupancy detected in the mailbox + Door opened recently: Discarding notification...")
      self.fire_event("NOTIFIER_DISCARD", tag = "you_got_mail")
  

  """
  Callback triggered when litter occupancy is detected
  Goals :
  . Increase litter tracking
  """
  def callback_litter_occupancy_detected(self, entity, attribute, old, new, kwargs):
    self.log("Occupancy detected in the litter. Incrementing litter tracking...")
    self.call_service("input_number/increment", entity_id = "input_number.litter_tracking")

  """
  Callback triggered when litter is full
  Goals :
  . notify is litter is full
  """
  def callback_litter_full(self, entity, attribute, old, new, kwargs):
    self.log("Litter full. notifying it ...")
    self.fire_event("NOTIFIER",
        action = "send_when_present",
        title = "🐈  Litière",
        message = "Penser a nettoyer la litière !",
        callback = [{
          "title" : "Litière Nettoyée",
          "event" : "reset_litter_tracking"}],
        icon =  "mdi:cat",
        color = "#ff6e07",
        persistent = True,
        tag = "litter_full",
        until =  [{
          "entity_id" : "binary_sensor.is_litter_full",
          "new_state" : "off"}])


  """
  Callback triggered when black trash can be taken out
  Goals :
  . Turn on input boolean to notify user on Home Assistant dashboard
  """
  def callback_black_trash_schedule_begining(self, entity, attribute, old, new, kwargs):
    self.log("It's time to take out black trash, turning on input boolean so it can be displayed on the dashboards ...")
    self.call_service("input_boolean/turn_on", entity_id = "input_boolean.poubelle_noire_a_sortir")
  
  """
  Callback triggered when green trash can be taken out
  Goals :
  . Turn on input boolean to notify user on Home Assistant dashboard
  """
  def callback_green_trash_schedule_begining(self, entity, attribute, old, new, kwargs):
    self.log("It's time to take out green trash, turning on input boolean so it can be displayed on the dashboards ...")
    self.call_service("input_boolean/turn_on", entity_id = "input_boolean.poubelle_verte_a_sortir")

  """
  Callback triggered when it's almost too late to take out black trash (and it's not yet done)
  Goals :
  . Notify present occupants
  """
  def callback_black_trash_schedule_end(self, entity, attribute, old, new, kwargs):
    if self.get_state("input_boolean.poubelle_noire_a_sortir") == "on":
      self.log("Black trash has not been taken out. Notifying it ...'")
      self.call_service("input_boolean/turn_off", entity_id = "input_boolean.poubelle_noire_a_sortir")
      self.fire_event("NOTIFIER",
        action = "send_to_present",
        title = "🗑 Poubelle Noire", 
        message = "N'oublie pas de sortir la poubelle noire",
        icon =  "mdi:delete",
        color = "#ff6e07",
        tag = "black_trash")

  """
  Callback triggered when it's almost too late to take out green trash (and it's not yet done)
  Goals :
  . Notify present occupants
  """
  def callback_green_trash_schedule_end(self, entity, attribute, old, new, kwargs):
    if self.get_state("input_boolean.poubelle_verte_a_sortir") == "on":
      self.log("Green trash has not been taken out. Notifying it ...'")
      self.call_service("input_boolean/turn_off", entity_id = "input_boolean.poubelle_verte_a_sortir")
      self.fire_event("NOTIFIER",
        action = "send_to_present",
        title = "♻️ Poubelle Verte", 
        message = "N'oublie pas de sortir la poubelle verte",
        icon =  "mdi:recycle",
        color = "#ff6e07",
        tag = "green_trash")

  """
  Callback triggered when Long press on entry switch (button ON)
  Goals :
  . Turn on lights
  """
  def callback_long_press_on_entry_switch_button_on(self, event_name, data, kwargs):
    self.log("Long press on entry switch (button ON), turning on lights ...")
    self.call_service("script/reset_lights_day_area")

  """
  Callback triggered when Long press on entry switch (button OFF)
  Goals :
  . Turn off lights, TV, KEF, coffee maker ...
  """
  def callback_long_press_on_entry_switch_button_off(self, event_name, data, kwargs):
    self.log("Long press on entry switch (button OFF), turning off lights, TV, KEF, coffee maker ...")
    self.call_service("script/leave_home")

  """
  Callback triggered when the service open_cover is called on cover.living_room_cover
  Goals :
  . If the over are already fully opened, press again the open button to tackle edge case of desynchronization between the different remotes.
  """
  def callback_cover_open_service_called(self, event_name, data, kwargs):
    if self.get_state("cover.living_room_cover") == "open" and self.get_state("cover.living_room_cover", attribute = "current_position") == 100:
      self.log("Action open cover fired, but cover already opened at 100%: Making sure they are opened")
      self.call_service("switch/turn_on" , entity_id = "switch.volet_salon_bouton_up_fallback")

  """
  Callback triggered when the service close_cover is called on cover.living_room_cover
  Goals :
  . If the over are already fully closed, press again the close button to tackle edge case of desynchronization between the different remotes.
  """
  def callback_cover_close_service_called(self, event_name, data, kwargs):
    if self.get_state("cover.living_room_cover") == "closed" and self.get_state("cover.living_room_cover", attribute = "current_position") == 0:
      self.log("Action close cover fired, but cover already closed at 0%: Making sure they are closed")
      self.call_service("switch/turn_on" , entity_id = "switch.volet_salon_bouton_down_fallback")

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

  """
  Callback triggered when button "reset_litter_tracking" is clicked from a notification
  Goals :
  . Reset Littter Tracking
  """
  def callback_button_clicked_reset_litter_tracking(self, event_name, data, kwargs):
    self.log("Notification button clicked : Resseting Litter Tracking")
    self.call_service("input_number/set_value" , entity_id = "input_number.litter_tracking", value = 0)