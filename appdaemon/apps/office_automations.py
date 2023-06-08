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
        self.listen_state(self.callback_presence_detected, "binary_sensor.office_presence_sensor_occupancy", new = "on")
        self.listen_state(self.callback_presence_not_detected, "binary_sensor.office_presence_sensor_occupancy", new = "off")
        self.listen_state(self.callback_vr_in_progress, "binary_sensor.quest_in_use", new = "on")
        self.listen_state(self.callback_vr_not_in_progress, "binary_sensor.quest_in_use", new = "off")
        
        
    def callback_webcam_in_use(self, entity, attribute, old, new, kwargs):
        is_jl_present = True if self.entities.person.jenova70.state == "home" else False
        is_jl_laptop_present = True if self.entities.device_tracker.jean_loics_laptop.state == "home" else False
        is_office_occupied = True if self.entities.binary_sensor.office_presence_sensor_occupancy.state == "on" else False

        if is_jl_present and is_jl_laptop_present and is_office_occupied:
            self.log("Webcam in use ... turning on face lights")
            self.call_service("light/turn_on", entity_id = "light.hue_play_bars", brightness_pct = 60)
    
    def callback_webcam_not_in_use(self, entity, attribute, old, new, kwargs):
        if self.entities.light.hue_play_bars.state == "on":
            self.log("Webcam not in use ... turning off face lights")
            self.call_service("light/turn_off", entity_id = "light.hue_play_bars")
    
    def callback_presence_detected(self, entity, attribute, old, new, kwargs):
        is_workday = True if self.entities.binary_sensor.workday_today.state == "on" else False
        is_working_hours = True if self.entities.schedule.working_hours.state == "on" else False
        is_jl_present = True if self.entities.person.jenova70.state == "home" else False

        if is_workday and is_working_hours and is_jl_present:
            self.log("Presence detected, during a working day and working hour... Turning on lights")
            self.call_service("light/turn_on", entity_id = "light.bureau", brightness_pct = 100)

    def callback_presence_not_detected(self, entity, attribute, old, new, kwargs):
        is_workday = True if self.entities.binary_sensor.workday_today.state == "on" else False
        is_working_hours = True if self.entities.schedule.working_hours.state == "on" else False
        is_jl_present = True if self.entities.person.jenova70.state == "home" else False

        if is_workday and is_working_hours and is_jl_present:
            self.log("Presence not detected, during a working day and working hour... Turning off lights")
            self.call_service("light/turn_off", entity_id = "light.bureau")
        
    def callback_vr_in_progress(self, entity, attribute, old, new, kwargs):
        is_jl_present = True if self.entities.person.jenova70.state == "home" else False
        is_office_occupied = True if self.entities.binary_sensor.office_presence_sensor_occupancy.state == "on" else False

        if is_jl_present and is_office_occupied:
            self.log("VR in progress... TODO")
            self.call_service("light/turn_on", entity_id = "light.hue_play_bars", brightness_pct = 100)
    
    def callback_vr_not_in_progress(self, entity, attribute, old, new, kwargs):
        is_jl_present = True if self.entities.person.jenova70.state == "home" else False
        is_office_occupied = True if self.entities.binary_sensor.office_presence_sensor_occupancy.state == "on" else False

        if is_jl_present and is_office_occupied:
            self.log("VR stopped... TODO")
            self.call_service("light/turn_off", entity_id = "light.hue_play_bars")

