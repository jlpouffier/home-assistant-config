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

    # Listen to presence_simulator_switch state change
    self.listen_state(self.callback_start_presence_simulation , "input_boolean.presence_simulator_switch" , new = "on", immediate = True)
    self.listen_state(self.callback_stop_presence_simulation , "input_boolean.presence_simulator_switch" , new = "off", immediate = True)

    # listen to home state change
    self.listen_state(self.callback_home_empty , "binary_sensor.home_occupied" ,  new = "off", immediate = True)
    self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" ,  new = "on", immediate = True)

    # listen to button press form notification
    self.listen_event(self.callback_button_clicked_start_presence_simulation, "mobile_app_notification_action", action = "start_presence_simulation")

    #Log
    self.log("Presence simulation Automations initialized" , log = 'user_log')
  
  """
  Callback triggered when the presence_simulator_switch is activated
  Goals :
  . Start the presence simulation routine
  """
  def callback_start_presence_simulation(self, entity, attribute, old, new, kwargs):
    self.log("Starting Presence Simulation" , log = 'user_log')
    self.timer_handles.append(self.run_daily(self.callback_wake_up, self.args["wake_up_time"]))
    self.timer_handles.append(self.run_daily(self.callback_eat_breakfast, self.args["eat_breakfast_time"]))
    self.timer_handles.append(self.run_daily(self.callback_leave, self.args["leave_time"]))
    self.timer_handles.append(self.run_daily(self.callback_return, self.args["return_time"]))
    self.timer_handles.append(self.run_daily(self.callback_go_to_bed, self.args["go_to_bed_time"]))
    self.timer_handles.append(self.run_daily(self.callback_sleep, self.args["sleep_time"]))

  """
  Callback triggered when the presence_simulator_switch is deactivated
  Goals :
  . Stop the presence simulation routine
  """
  def callback_stop_presence_simulation(self, entity, attribute, old, new, kwargs):
    self.log("Stoping Presence Simulation" , log = 'user_log')
    while len(self.timer_handles) >=1:
      handle = self.timer_handles.pop()
      self.cancel_timer(handle)


  """
  Callback triggered when the home is empty
  Goals :
  . Start to listen to far_away event
  """
  def callback_home_empty(self, entity, attribute, old, new, kwargs):
    self.log("Home empty, starting to listen for far_away event to enable presence simulation" , log = 'user_log')
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
      self.log("Home occupied, stopping to listen for far_away event" , log = 'user_log')
      self.cancel_listen_state(self.callback_occupants_far_away_handle)
    
    if self.get_state("input_boolean.presence_simulator_switch") == "on":
      self.log("Stopping Presence Simulator" , log = 'user_log')
      self.call_service("input_boolean/toggle", entity_id = "input_boolean.presence_simulator_switch")
    
  """
  Callback triggered when the occupants are all far away
  Goals :
  . Notify them to turn on presence simulation
  """
  def callback_occupants_far_away(self, entity, attribute, old, new, kwargs):
    self.callback_occupants_far_away_enabled = False
    if self.get_state("input_boolean.presence_simulator_switch") == "off":
      self.log("Occupant far away and presence simulation not activated... Notifying it ... (once)" , log = 'user_log')
      self.fire_event("NOTIFIER",
        action = "send_to_nearest",
        title = "🌍 Vous etes loin", 
        message = "Vous vous trouvez loin du domicile, activer la simulation de présence?",
        callback = [{
          "title" : "simuler une présence",
          "event" : "start_presence_simulation"}],
        click_url="/lovelace/apercu",
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
    self.log("Notification button clicked : Starting Presence Simulation" , log = 'user_log') 
    self.call_service("input_boolean/turn_on" , entity_id = "input_boolean.presence_simulator_switch")


  """
  Callback triggered near wake up time.
  Goals :
  . Turn on bedroom lights
  """
  def callback_wake_up(self, kwargs):
    self.log("Simulating : Waking up" , log = 'user_log')
    self.call_service("light/turn_on" , entity_id = "light.chambre", brightness_pct = 100)
    
  """
  Callback triggered near breakfast time. 
  Goals :
  . Turn off bedroom lights
  . Turn on living room lights
  . Turn on kitchen lights

  """
  def callback_eat_breakfast(self, kwargs):
    self.log("Simulating : Eating Breakfast" , log = 'user_log')
    self.call_service("light/turn_off" , entity_id = "light.chambre")
    self.call_service("hue/activate_scene" , entity_id = "scene.salon_salon_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.cuisine_cuisine_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.entree_entree_100")
    
  """
  Callback triggered near "leaving" time.
  Goals :
  . Turn off all lights
  """
  def callback_leave(self, kwargs):
    self.log("Simulating : Leaving home" , log = 'user_log')
    self.call_service("light/turn_off" , entity_id = "light.all_lights")

    
  """
  Callback triggered near "retunring" time.
  Goals :
  . Turn on exterior lights
  . Turn on living room lights
  . Turn on kitchen lights
  """
  def callback_return(self, kwargs):
    self.log("Simulating : Returning home" , log = 'user_log')
    self.call_service("hue/activate_scene" , entity_id = "scene.salon_salon_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.cuisine_cuisine_100")
    self.call_service("hue/activate_scene" , entity_id = "scene.entree_entree_100")
    
  """
  Callback triggered near bed time.
  Goals :
  . Turn off exterior lights
  . Turn off living room lights
  . Turn off kitchen lights
  . Turn on bedroom lights
  """
  def callback_go_to_bed(self, kwargs):
    self.log("Simulating : Going to bed" , log = 'user_log')
    self.call_service("light/turn_off" , entity_id = "light.salon") 
    self.call_service("light/turn_off" , entity_id = "light.cuisine")
    self.call_service("light/turn_off" , entity_id = "light.entree")
    self.call_service("hue/activate_scene" , entity_id = "scene.chambre_chambre_100")

  """
  Callback triggered near sleep time.
  Goals :
  . Turn off all lights
  """
  def callback_sleep(self, kwargs):
    self.log("Simulating : Sleeping" , log = 'user_log')
    self.call_service("light/turn_off" , entity_id = "light.all_lights")