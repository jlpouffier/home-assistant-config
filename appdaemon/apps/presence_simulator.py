import hassapi as hass
import datetime

"""
presence_simulator is an app responsible of simulating the presence of humans in our appartment when we are not present

Functionalities :
. Turn on and off lights at different (randomized) time

"""
class presence_simulator(hass.Hass): 
  def initialize(self):

    # Define times
    wake_up_time = datetime.time(7,0,0)
    eat_breakfast_time = datetime.time(8,0,0)
    leave_time = datetime.time(9,0,0)
    return_time = datetime.time(20,0,0)
    go_to_bed_time = datetime.time(22,0,0)
    sleep_time = datetime.time(23,0,0)

    # Define random off-set
    random_offset = 15*60

    # Declare all callbacks
    self.run_daily(self.callback_wake_up, wake_up_time, random_start = -random_offset, random_end = random_offset)
    self.run_daily(self.callback_eat_breakfast, eat_breakfast_time, random_start = -random_offset, random_end = random_offset)
    self.run_daily(self.callback_leave, leave_time, random_start = -random_offset, random_end = random_offset)
    self.run_daily(self.callback_return, return_time, random_start = -random_offset, random_end = random_offset)
    self.run_daily(self.callback_go_to_bed, go_to_bed_time, random_start = -random_offset, random_end = random_offset)
    self.run_daily(self.callback_sleep, sleep_time, random_start = -random_offset, random_end = random_offset) 

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




  
