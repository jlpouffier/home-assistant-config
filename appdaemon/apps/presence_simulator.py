import hassapi as hass
import datetime

"""
presence_simulator is an app responsible of simulating the presence of humans in our appartment when we are not present

Functionalities :
. Turn on and off lights at different (randomized) time

"""
class presence_simulator(hass.Hass): 
  def initialize(self):
    # Storage for simulation handles 
    self.timer_handles = []

    # variable to handle the far_away notification
    self.callback_occupants_far_away_enabled = False

    # Listen to automation_presence_simulator state change
    self.listen_state(self.callback_start_presence_simulation , "input_boolean.automation_presence_simulator" , new = "on", immediate = True)
    self.listen_state(self.callback_stop_presence_simulation , "input_boolean.automation_presence_simulator" , new = "off", immediate = True)

    # listen to home state change
    self.listen_state(self.callback_home_empty , "binary_sensor.home_occupied" ,  new = "off", immediate = True)
    self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" ,  new = "on", immediate = True)

    # listen to button press form notification
    self.listen_event(self.callback_button_clicked_start_presence_simulation, "mobile_app_notification_action", action = "start_presence_simulation")
  
  """
  Callback triggered when the automation_presence_simulator is activated
  Goals :
  . Start the presence simulation routine
  """
  def callback_start_presence_simulation(self, entity, attribute, old, new, kwargs):
    self.log("Starting Presence Simulation")
    random_offset_seconds = 60 * self.args["random_offset"]
    self.timer_handles.append(self.run_daily(self.callback_wake_up, self.args["wake_up_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds))
    self.timer_handles.append(self.run_daily(self.callback_eat_breakfast, self.args["eat_breakfast_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds))
    self.timer_handles.append(self.run_daily(self.callback_leave, self.args["leave_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds))
    self.timer_handles.append(self.run_daily(self.callback_return, self.args["return_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds))
    self.timer_handles.append(self.run_daily(self.callback_go_to_bed, self.args["go_to_bed_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds))
    self.timer_handles.append(self.run_daily(self.callback_sleep, self.args["sleep_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds))

  """
  Callback triggered when the automation_presence_simulator is deactivated
  Goals :
  . Stop the presence simulation routine
  """
  def callback_stop_presence_simulation(self, entity, attribute, old, new, kwargs):
    self.log("Stoping Presence Simulation")
    while len(self.timer_handles) >=1:
      handle = self.timer_handles.pop()
      self.cancel_timer(handle)


  """
  Callback triggered when the home is empty
  Goals :
  . Start to listen to far_away event
  """
  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    self.log("Home empty, starting to listen for far_away event to enable presence simulation")
    self.callback_occupants_far_away_enabled = True
    self.callback_occupants_far_away_handle = self.listen_state(self.callback_occupants_far_away , "binary_sensor.far_away" , new = "on", oneshot = True)

  """
  Callback triggered when the home is occupied
  Goals :
  . If needed stop listening to far_away event
  . If needed stop presence simulation
  """
  def callback_home_occupied(self, entity, attribute, old, new, kwargs):
    if self.callback_occupants_far_away_enabled:
      self.log("Home occupied, stopping to listen for far_away event")
      self.cancel_listen_state(self.callback_occupants_far_away_handle)
    
    if self.entities.input_boolean.automation_presence_simulator.state == "on":
      self.log("Stopping Presence Simulator")
      self.call_service("input_boolean/toggle", entity_id = "input_boolean.automation_presence_simulator")
    
  """
  Callback triggered when the occupants are all far away
  Goals :
  . Notify them to turn on presence simulation
  """
  def callback_occupants_far_away(self, entity, attribute, old, new, kwargs):
    self.callback_occupants_far_away_enabled = False
    if self.entities.input_boolean.automation_presence_simulator.state == "off":
      self.log("Occupant far away and presence simulation not activated... Notifying it ... (once)")
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "🌍 Vous etes loin", 
        message = "Vous vous trouvez loin du domicile, activer la simulation de présence?",
        callback = [{
          "title" : "simuler une présence",
          "event" : "start_presence_simulation"}],
        click_url="/dashboard-automatisations/automatisations",
        icon =  "mdi:compass",
        tag = "far_away",
        until =  [{
          "entity_id" : "binary_sensor.home_occupied",
          "new_state" : "on"}])

  """
  Callback triggered when button "start_presence_simulation" is clicked from a notification
  Goals :
  . Start Presence Simulation
  """
  def callback_button_clicked_start_presence_simulation(self, event_name, data, kwargs):
    self.log("Notification button clicked : Starting Presence Simulation") 
    self.call_service("input_boolean/turn_on" , entity_id = "input_boolean.automation_presence_simulator")


  """
  Callback triggered near wake up time.
  Goals :
  . Turn on bedrooms lights
  """
  def callback_wake_up(self, kwargs):
    self.log("Simulating : Waking up")
    self.call_service("hue/activate_scene" , entity_id = "scene.chambre_chambre_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.bureau_bureau_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.chambre_bebe_chambre_bebe_100")
    
  """
  Callback triggered near breakfast time. 
  Goals :
  . Turn off bedrooms lights
  . Turn on living room lights
  . Turn on kitchen lights

  """
  def callback_eat_breakfast(self, kwargs):
    self.log("Simulating : Eating Breakfast")
    self.call_service("light/turn_off" , entity_id = "light.chambre")
    self.call_service("light/turn_off" , entity_id = "light.chambre_bebe")
    self.call_service("light/turn_off" , entity_id = "light.bureau")
    self.call_service("hue/activate_scene" , entity_id = "scene.salon_salon_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.cuisine_cuisine_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.entree_entree_100")

    if self.entities.input_boolean.presence_simulator_control_cover.state == "on":
      self.call_service("cover/open_cover", entity_id = "cover.living_room_cover")
    
  """
  Callback triggered near "leaving" time.
  Goals :
  . Turn off all lights
  """
  def callback_leave(self, kwargs):
    self.log("Simulating : Leaving home")
    self.call_service("light/turn_off" , entity_id = "light.all_lights")

    if self.entities.input_boolean.presence_simulator_control_cover.state == "on":
      self.call_service("cover/close_cover", entity_id = "cover.living_room_cover")

    
  """
  Callback triggered near "retunring" time.
  Goals :
  . Turn on exterior lights
  . Turn on living room lights
  . Turn on kitchen lights
  """
  def callback_return(self, kwargs):
    self.log("Simulating : Returning home")
    self.call_service("hue/activate_scene" , entity_id = "scene.salon_salon_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.cuisine_cuisine_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.entree_entree_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.exterieur_exterieur_100")

    if self.entities.input_boolean.presence_simulator_control_cover.state == "on":
      self.call_service("cover/open_cover", entity_id = "cover.living_room_cover")
    
  """
  Callback triggered near bed time.
  Goals :
  . Turn off exterior lights
  . Turn off living room lights
  . Turn off kitchen lights
  . Turn on bedrooms lights
  """
  def callback_go_to_bed(self, kwargs):
    self.log("Simulating : Going to bed")
    self.call_service("light/turn_off" , entity_id = "light.salon") 
    self.call_service("light/turn_off" , entity_id = "light.cuisine")
    self.call_service("light/turn_off" , entity_id = "light.entree")
    self.call_service("light/turn_off" , entity_id = "light.exterieur")
    self.call_service("hue/activate_scene" , entity_id = "scene.chambre_chambre_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.bureau_bureau_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.chambre_bebe_chambre_bebe_100")

    if self.entities.input_boolean.presence_simulator_control_cover.state == "on":
      self.call_service("cover/close_cover", entity_id = "cover.living_room_cover")
    

  """
  Callback triggered near sleep time.
  Goals :
  . Turn off all lights
  """
  def callback_sleep(self, kwargs):
    self.log("Simulating : Sleeping")
    self.call_service("light/turn_off" , entity_id = "light.all_lights")