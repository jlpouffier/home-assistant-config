import hassapi as hass

"""
baby_automations is an app responsible of tracking pee, poo and feed time of our future little cutre devil. 
"""
class baby_automations(hass.Hass):
    def initialize(self):
        self.listen_state(self.callback_change_button_clicked, "sensor.bouton_change_bebe_action", new = "press")
        self.listen_state(self.callback_bottle_button_clicked, "sensor.bouton_bibi_bebe_action", new = "press")
        self.listen_state(self.callback_bottle_button_clicked, "input_button.bouton_bibi_bebe_virtuel")
        self.listen_state(self.callback_change_pee_selected, "input_select.bebe_change_types", new = "pipi", duration = 5)
        self.listen_state(self.callback_change_poo_selected, "input_select.bebe_change_types", new = "caca", duration = 5)
        self.listen_state(self.callback_change_mode_cycle, "input_select.bebe_change_types")
        self.call_service("scene/create", scene_id =  "scene_current_hue_play_bars_state" , snapshot_entities = "light.hue_play_bars")
    
        self.log("Initialized")

    def callback_change_button_clicked(self, entity, attribute, old, new, kwargs):
        self.log("Baby Change: Button Pressed")
        if self.get_state("input_select.bebe_change_types") == "-":
            self.call_service("scene/create", scene_id =  "scene_current_hue_play_bars_state" , snapshot_entities = "light.hue_play_bars")
        self.call_service("input_select/select_next", entity_id = "input_select.bebe_change_types", cycle = True)
    
    def callback_bottle_button_clicked(self, entity, attribute, old, new, kwargs):
        self.log("Baby Feeding: Button Pressed")
        now = self.get_now()
        self.call_service("google/create_event", entity_id = "calendar.bebe_stats", summary = "🍼 Bibi", start_date_time = now, end_date_time = now )


    def callback_change_pee_selected(self, entity, attribute, old, new, kwargs):
        self.log("Baby Change: Pee selected")
        now = self.get_now()
        self.call_service("google/create_event", entity_id = "calendar.bebe_stats", summary = "💦 Pipi", start_date_time = now, end_date_time = now )
        self.call_service("input_select/select_first", entity_id = "input_select.bebe_change_types")
    
    def callback_change_poo_selected(self, entity, attribute, old, new, kwargs):
        self.log("Baby Change: Poo selected")
        now = self.get_now()
        self.call_service("google/create_event", entity_id = "calendar.bebe_stats", summary = "🎁 Caca", start_date_time = now, end_date_time = now )
        self.call_service("input_select/select_first", entity_id = "input_select.bebe_change_types")
    
    def callback_change_mode_cycle(self, entity, attribute, old, new, kwargs):
        if self.get_state("binary_sensor.home_occupied") == "on":
            if new == "-":
                self.call_service("scene/turn_on", entity_id = "scene.scene_current_hue_play_bars_state")
            elif new == "pipi":
                self.call_service("light/turn_on", entity_id = "light.hue_play_bars", color_name = "yellow", brightness_pct = 50)
            elif new == "caca":
                self.call_service("light/turn_on", entity_id = "light.hue_play_bars", color_name = "chocolate", brightness_pct = 50)