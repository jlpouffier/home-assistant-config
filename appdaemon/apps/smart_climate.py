import hassapi as hass
import datetime

"""
smart_climate is an app responsible of 

Functionalities :
. Automaitcally turn-off Climate after 2 hours of being on.


"""
class smart_climate(hass.Hass):
  def initialize(self):
    # List the Climates and Modes to listen to 
    modes_to_listen = ["cool", "heat", "fan_only", "dry", "heat_cool"]
    climates_to_listen = ["climate.salon", "climate.chambre", "climate.bureau"]

    # Register the maximum allowed time for a climate to be ON
    max_time_on = 2 * 60 * 60

    # Register "Delayed" callbacks (triggered if a Climate run for more than the allowed time)
    for climate in climates_to_listen:
      for mode in modes_to_listen:
        self.listen_state(self.callback_stop_climate, climate , new = mode , duration = max_time_on)

    self.log("Smart Climate Automations initialized")

  """
  Callback trigerred if a climate is on for too long
  Goals
  . Turn off Climate
  """
  def callback_stop_climate(self, entity, attribute, old, new, kwargs):
    self.log("Climate on since a long time, turning it off...")
    self.call_service("climate/turn_off", entity_id = entity)