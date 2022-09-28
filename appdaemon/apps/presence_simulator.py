import hassapi as hass
import datetime

"""
presence_simulator is an app responsible of simulating the presence of humans in our appartment when we are not present

Functionalities :
. Turn on and off lights at different (randomized) time

"""
class presence_simulator(hass.Hass): 
  def initialize(self):
    # Define random off-set
    random_offset_seconds = 60 * self.args["random_offset"] 

    # Declare all callbacks
    self.run_daily(self.callback_wake_up, self.args["wake_up_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds)
    self.run_daily(self.callback_eat_breakfast, self.args["eat_breakfast_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds)
    self.run_daily(self.callback_leave, self.args["leave_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds)
    self.run_daily(self.callback_return, self.args["return_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds)
    self.run_daily(self.callback_go_to_bed, self.args["go_to_bed_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds)
    self.run_daily(self.callback_sleep, self.args["sleep_time"], random_start = -random_offset_seconds, random_end = random_offset_seconds) 

    #Log
    self.log("Presence simulation Automations initialized")

  """
  Callback triggered near wake up time.
  Goals :
  . Turn on bedroom lights
  """
  def callback_wake_up(self, kwargs):
    self.log("Simulating : Waking up")
    self.call_service("light/turn_on" , entity_id = "light.chambre", brightness_pct = 100)
    
  """
  Callback triggered near breakfast time. 
  Goals :
  . Turn off bedroom lights
  . Turn on living room lights
  . Turn on kitchen lights

  """
  def callback_eat_breakfast(self, kwargs):
    self.log("Simulating : Eating Breakfast")
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
    self.log("Simulating : Leaving home")
    self.call_service("light/turn_off" , entity_id = "light.all_lights")

    
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
    
  """
  Callback triggered near bed time.
  Goals :
  . Turn off exterior lights
  . Turn off living room lights
  . Turn off kitchen lights
  . Turn on bedroom lights
  """
  def callback_go_to_bed(self, kwargs):
    self.log("Simulating : Going to bed")
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
    self.log("Simulating : Sleeping")
    self.call_service("light/turn_off" , entity_id = "light.all_lights")