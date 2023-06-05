import hassapi as hass
import datetime

"""
office_automations is an app responsible of managing my home office workspace

Functionalities :
. Turn on webcam light when I am on a call

"""
class office_automations(hass.Hass): 
    def initialize(self):
        self.listen_state(self.callback_webcam_in_use, "binary_sensor.jean_loics_laptop_camera_in_use", new = "on")
        self.listen_state(self.callback_webcam_not_in_use, "binary_sensor.jean_loics_laptop_camera_in_use", new = "off")
    
    def callback_webcam_in_use(self, entity, attribute, old, new, kwargs):
        self.log("Webcam in use ... turning on face lights")
        self.call_service("light/turn_on", entity_id = "light.hue_play_bars", brightness_pct = 70)
    
    def callback_webcam_not_in_use(self, entity, attribute, old, new, kwargs):
        self.log("Webcam not in use ... turning off face lights")
        self.call_service("light/turn_off", entity_id = "light.hue_play_bars")
    