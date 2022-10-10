import hassapi as hass

class track_car(hass.Hass):
    def initialize(self):
        self.log("tracking car automations initialized")
        self.listen_state(self.callback_start_high_accuracy_geolocation, "binary_sensor.clio_used_by_jl", attribute = "will_soon_turn_off", old = False, new = True)
        self.listen_state(self.callback_start_high_accuracy_geolocation, "binary_sensor.clio_used_by_valentine", attribute = "will_soon_turn_off", old = False, new = True)
        self.listen_state(self.callback_stop_high_accuracy_geolocation, "binary_sensor.clio_used_by_jl", attribute = "will_soon_turn_off", old = True, new = False)
        self.listen_state(self.callback_stop_high_accuracy_geolocation, "binary_sensor.clio_used_by_valentine", attribute = "will_soon_turn_off", old = True, new = False)
        
    def callback_start_high_accuracy_geolocation(self, entity, attribute, old, new, kwargs):
        if entity == "binary_sensor.clio_used_by_jl":
            service = "notify/mobile_app_pixel_6"
            name = "JL"
        elif entity == "binary_sensor.clio_used_by_valentine":
            service = "notify/mobile_app_pixel_4a"
            name = "Valentine"
        data = {
            "command":"turn_on",
            "ttl": "0",
            "priority": "high"
        }
        if self.get_state("binary_sensor.clio_v2") == "on":
            self.log(name + " just left clio, starting high accuracy mode ...")
            self.call_service(service, message = "command_high_accuracy_mode" , data = data)

    def callback_stop_high_accuracy_geolocation(self, entity, attribute, old, new, kwargs):
        if entity == "binary_sensor.clio_used_by_jl":
            service = "notify/mobile_app_pixel_6"
        elif entity == "binary_sensor.clio_used_by_valentine":
            service = "notify/mobile_app_pixel_4a"
        self.log("Stopping high accuracy mode ...")  
        data = {
            "command":"turn_off",
            "ttl": "0",
            "priority": "high"
        }
        self.call_service(service, message = "command_high_accuracy_mode" , data = data)