import hassapi as hass

class take_out_trash(hass.Hass):
    def initialize(self):
        self.log("Trash automations initialized ... ")
        self.listen_state(self.callback_black_trash_schedule_begining, "schedule.planning_poubelle_noire", new = "on")
        self.listen_state(self.callback_green_trash_schedule_begining, "schedule.planning_poubelle_verte", new = "on")
        self.listen_state(self.callback_black_trash_schedule_end, "schedule.planning_poubelle_noire", new = "off")
        self.listen_state(self.callback_green_trash_schedule_end, "schedule.planning_poubelle_verte", new = "off")
        
    
    def callback_black_trash_schedule_begining(self, entity, attribute, old, new, kwargs):
        self.call_service("input_boolean/turn_on", entity_id = "input_boolean.poubelle_noire_a_sortir")
    
    def callback_green_trash_schedule_begining(self, entity, attribute, old, new, kwargs):
        self.call_service("input_boolean/turn_on", entity_id = "input_boolean.poubelle_verte_a_sortir")

    def callback_black_trash_schedule_end(self, entity, attribute, old, new, kwargs):
        if self.get_state("input_boolean.poubelle_noire_a_sortir") == "on":
            self.log("Black trash has not been taken out. Notifying it ...'")
            self.call_service("input_boolean/turn_off", entity_id = "input_boolean.poubelle_noire_a_sortir")
            self.fire_event("NOTIFIER",
                action = "send_to_present",
                title = "🗑 Poubelle Noire", 
                message = "N'oublie pas de sortir la poubelle noire",
                icon =  "mdi:delete",
                color = "#ff6e07",
                tag = "black_trash")
    
    def callback_green_trash_schedule_end(self, entity, attribute, old, new, kwargs):
        if self.get_state("input_boolean.poubelle_verte_a_sortir") == "on":
            self.log("Green trash has not been taken out. Notifying it ...'")
            self.call_service("input_boolean/turn_off", entity_id = "input_boolean.poubelle_verte_a_sortir")
            self.fire_event("NOTIFIER",
                action = "send_to_present",
                title = "♻️ Poubelle Verte", 
                message = "N'oublie pas de sortir la poubelle verte",
                icon =  "mdi:recycle",
                color = "#ff6e07",
                tag = "green_trash")