import hassapi as hass

"""
smart_hue_buttons extend the functionalities of my hue buttons

Functionalities :
    Entry hue switch
        Long press on I : Turn on all first floor lights
        Long press on O : Turn on all lights, coffee maker, TV, KEF 
    
    LivingRoom Coridor switch
        Long Press on I : Turn on all first floor lights
        Long Press on O : Turn off all first floor lights

Notifications :
. None

"""
class smart_hue_buttons(hass.Hass): 
    def initialize(self):
        self.listen_event(self.callback_long_press_on_entry_switch_button_on, "hue_event", device_id = "64185ca2086c2ebd7b976a43ef0c89fd", unique_id = "c1c9f277-e27a-4340-9962-2206cc0d7e3a", type = "long_release", subtype = 1)
        self.listen_event(self.callback_long_press_on_entry_switch_button_off, "hue_event", device_id = "64185ca2086c2ebd7b976a43ef0c89fd", unique_id = "7564eab9-3cc9-4321-890c-1b9f1465f108", type = "long_release", subtype = 4)
        self.listen_event(self.callback_long_press_on_living_room_coridor_switch_button_on, "hue_event", device_id = "efa42240bac38d83b77963e7fd5bb5ac", unique_id = "9df3f0e5-001b-4c7b-9c5d-a96a8b391edd", type = "long_release", subtype = 1)
        self.listen_event(self.callback_long_press_on_living_room_coridor_switch_button_off, "hue_event", device_id = "efa42240bac38d83b77963e7fd5bb5ac", unique_id = "73e97207-29d2-4078-8304-9e918425fe48", type = "long_release", subtype = 4)
        

    """
    Callback triggered when Long press on entry switch (button ON)
    Goals :
    . Turn on lights
    """
    def callback_long_press_on_entry_switch_button_on(self, event_name, data, kwargs):
        self.log("Long press on entry switch (button ON), turning on lights ...")
        self.call_service("script/reset_lights_day_area")

    """
    Callback triggered when Long press on entry switch (button OFF)
    Goals :
    . Turn off lights, TV, KEF, coffee maker ...
    """
    def callback_long_press_on_entry_switch_button_off(self, event_name, data, kwargs):
        self.log("Long press on entry switch (button OFF), turning off lights, TV, KEF, coffee maker ...")
        self.call_service("script/leave_home")

    """
    Callback triggered when Long press on living room / coridor switch (button ON)
    Goals :
    . Turn on lights
    """
    def callback_long_press_on_living_room_coridor_switch_button_on(self, event_name, data, kwargs):
        self.log("Long press on living room / coridor switch (button ON), turning on lights ...")
        self.call_service("script/reset_lights_day_area")

    """
    Callback triggered when Long press on living room / coridor switch (button OFF)
    Goals :
    . Turn off lights
    """
    def callback_long_press_on_living_room_coridor_switch_button_off(self, event_name, data, kwargs):
        self.log("Long press on living room / coridor switch (button OFF), turning off lights ...")
        self.call_service("light/turn_off", entity_id = "light.lumieres_rez_de_chaussee")