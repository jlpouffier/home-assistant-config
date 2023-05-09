import hassapi as hass

class matrix_2d(hass.Hass):
    def initialize(self):
        self.listen_state(self.callback_state_change)
        self.listen_event(self.callback_event, ["google_assistant_query", "alexa_smart_home"])
        self.listen_event(self.callback_event, "hue_event", type = "initial_press" )
        
    
    def callback_state_change(self, entity, attribute, old, new, kwargs):
        if self.is_in_scope(entity) and self.entities.binary_sensor.home_occupied.state == "on":
            self.call_service("script/pulse_2d_led_matrix") 
    
    def callback_event(self, event_name, data, kwargs):
        if self.entities.binary_sensor.home_occupied.state == "on":
            self.call_service("script/pulse_2d_led_matrix") 

    def is_in_scope(self, entity):
        domain_excluded = False
        entity_included = False
        entity_excluded = False

        domain = entity.split(".")[0]

        if domain in self.args["excluded_domains"]:
            domain_excluded = True
        if entity in self.args["included_entities"]:
            entity_included = True
        if entity in self.args["excluded_entities"]:
            entity_excluded = True
        
        if entity == "light.2d_matrix" or entity == "script.pulse_2d_led_matrix":
            return False
        elif entity_included:
            return True
        elif entity_excluded:
            return False
        elif domain_excluded:
            return False
        else:
            return True