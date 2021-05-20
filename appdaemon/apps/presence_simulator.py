import hassapi as hass
import datetime

"""
presence_simulator is an app responsible of 

Goals :
. 

Notifications :
. 


"""
class presence_simulator(hass.Hass): 
  def initialize(self):
  	wake_up_time = datetime.time(7,0,0)
  	eat_breakfast_time = datetime.time(8,0,0)
  	leave_time = datetime.time(9,0,0)
  	return_time = datetime.time(20,0,0)
  	go_to_bed_time = datetime.time(22,0,0)
  	sleep_time = datetime.time(23,0,0)

  	random_offset = 15*60

  	self.run_daily(self.callback_wake_up, wake_up_time, random_start = -random_offset, random_end = random_offset)
  	self.run_daily(self.callback_eat_breakfast, eat_breakfast_time, random_start = -random_offset, random_end = random_offset)
  	self.run_daily(self.callback_leave, leave_time, random_start = -random_offset, random_end = random_offset)
  	self.run_daily(self.callback_return, return_time, random_start = -random_offset, random_end = random_offset)
  	self.run_daily(self.callback_go_to_bed, go_to_bed_time, random_start = -random_offset, random_end = random_offset)
  	self.run_daily(self.callback_sleep, sleep_time, random_start = -random_offset, random_end = random_offset) 

  	self.log("Presence simulation Automations initialized")

  def callback_wake_up(self, kwargs):
  	self.log("Simulating : Waking up")
  	#self.call_service("light/turn_on" , entity_id = "light.chambre_principale", brightness_pct = 100)
  	

  def callback_eat_breakfast(self, kwargs):
  	self.log("Simulating : Eating Breakfast")
  	#self.call_service("light/turn_off" , entity_id = "light.chambre_principale")
  	#self.call_service("light/turn_on" , entity_id = "light.salon", brightness_pct = 100)
  	#self.call_service("light/turn_on" , entity_id = "light.cuisine", brightness_pct = 100)
  	

  def callback_leave(self, kwargs):
  	self.log("Simulating : Leaving home")
  	#self.call_service("light/turn_off" , entity_id = "light.interior_lights")
  	#self.call_service("light/turn_off" , entity_id = "light.exterior_lights")

  	

  def callback_return(self, kwargs):
  	self.log("Simulating : Returning home")
  	#self.call_service("light/turn_on" , entity_id = "light.salon", brightness_pct = 100)
  	#self.call_service("light/turn_on" , entity_id = "light.cuisine", brightness_pct = 100)
  	#self.call_service("light/turn_on" , entity_id = "light.terrasse", brightness_pct = 100)
  	

  def callback_go_to_bed(self, kwargs):
  	self.log("Simulating : Going to bed")
  	#self.call_service("light/turn_off" , entity_id = "light.salon")
  	#self.call_service("light/turn_off" , entity_id = "light.cuisine")
  	#self.call_service("light/turn_off" , entity_id = "light.terrasse")
  	#self.call_service("light/turn_on" , entity_id = "light.chambre_principale", brightness_pct = 100)
  	

  def callback_sleep(self, kwargs):
  	self.log("Simulating : Sleeping")
  	#self.call_service("light/turn_off" , entity_id = "light.interior_lights")
  	#self.call_service("light/turn_off" , entity_id = "light.exterior_lights")
  	



  
