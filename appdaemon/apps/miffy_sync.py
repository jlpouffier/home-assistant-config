import hassapi as hass
import datetime

"""
miffy_sync is an app responsible of syncing miffy ligth with other lights in the room

Functionalities :
    Sync the miffy light to other light in the bedroom

Notifications :
    None
"""
class miffy_sync(hass.Hass):
    def initialize(self):
        self.listen_state(self.callback_light_on, "light.chambre_bebe_suspension", new = "on")
        self.listen_state(self.callback_light_off, "light.chambre_bebe_suspension", new = "off")
        self.listen_state(self.callback_brightness_updated, "light.chambre_bebe_suspension", attribute = "brightness")
    
    def callback_light_on(self, entity, attribute, old, new, kwargs):
        try:
            target_brightness = self.entities.light.chambre_bebe_suspension.attribute.brightness
        except:
            target_brightness = 100
        self.call_service("light/turn_on", entity_id = "light.miffy", brightness = target_brightness)
    
    def callback_light_off(self, entity, attribute, old, new, kwargs):
        self.call_service("light/turn_off", entity_id = "light.miffy")
    
    def callback_brightness_updated(self, entity, attribute, old, new, kwargs):
        if new is not None:
            self.call_service("light/turn_on", entity_id = "light.miffy", brightness = new)
