import hassapi as hass
import datetime

"""
smart_climate is an app responsible of 

Goals :
. 

Notifications :
. 


"""
class smart_climate(hass.Hass):
  def initialize(self):
    modes_to_listen = ["cool", "heat", "fan_only", "dry", "heat_cool"]
    climates_to_listen = ["climate.salon", "climate.chambre", "climate.bureau"]
    max_time_on = 2 * 60 * 60

    for climate in climates_to_listen:
      for mode in modes_to_listen:
        self.listen_state(self.callback_stop_climate, climate , new = mode , duration = max_time_on)

    self.log("Smart Climate Automations initialized")


  def callback_stop_climate(self, entity, attribute, old, new, kwargs):
    self.log("Climate on since a long time, turning it off...")
    self.call_service("climate/turn_off", entity_id = entity)