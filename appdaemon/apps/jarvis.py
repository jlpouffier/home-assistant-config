import hassapi as hass

class jarvis(hass.Hass):
    def initialize(self):
        self.listen_event(self.callback_act_on_switch_entity, "rhasspy_act_on_switch_entity")
        self.listen_event(self.callback_act_on_light_entity, "rhasspy_act_on_light_entity")
        self.listen_event(self.callback_act_on_cover_entity, "rhasspy_act_on_cover_entity")
        self.listen_event(self.callback_act_on_cover_position_entity, "rhasspy_act_on_cover_position_entity")

        self.log("Initialized")
    
    def callback_act_on_switch_entity(self, event_name, data, kwargs):
        self.log("callback_act_on_switch_entity")
        self.call_service(data["action"], entity_id = data["entity"])
    
    def callback_act_on_light_entity(self, event_name, data, kwargs):
        self.log("callback_act_on_light_entity")
        if data["action"] == "light/turn_on":
            self.call_service(data["action"], entity_id = data["entity"], brightness_pct = 100)
        else:
            self.call_service(data["action"], entity_id = data["entity"])

    def callback_act_on_cover_entity(self, event_name, data, kwargs):
        self.log("callback_act_on_cover_entity")
        self.call_service(data["action"], entity_id = "cover.living_room_cover")
    
    def callback_act_on_cover_position_entity(self, event_name, data, kwargs):
        self.log("callback_act_on_cover_position_entity")
        self.call_service("cover/set_cover_position", entity_id = "cover.living_room_cover", position = data["position"])
