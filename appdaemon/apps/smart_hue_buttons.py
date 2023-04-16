import hassapi as hass

"""
smart_hue_buttons extend the functionalities of my hue buttons

Functionalities :
    Entry hue switch
        Long press on I : Turn on all first flor lights
        Long press on O : Turn on all lights, coffee maker, TV, KEF 

Notifications :
. None

"""
class smart_hue_buttons(hass.Hass): 
    def initialize(self):
        self.listen_event(self.callback_long_press_on_entry_switch_button_on, "hue_event", device_id = "64185ca2086c2ebd7b976a43ef0c89fd", unique_id = "c1c9f277-e27a-4340-9962-2206cc0d7e3a", type = "repeat", subtype = 1)
        self.listen_event(self.callback_long_press_on_entry_switch_button_off, "hue_event", device_id = "64185ca2086c2ebd7b976a43ef0c89fd", unique_id = "7564eab9-3cc9-4321-890c-1b9f1465f108", type = "repeat", subtype = 4)

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