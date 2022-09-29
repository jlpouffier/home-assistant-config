import hassapi as hass

class smart_cube(hass.Hass):
    def initialize(self):
        self.global_handles = []
        self.mode_handles = []
        self.current_light = ""
        self.current_vacuum = ""
        self.current_tv_source = ""

        self.listen_state(self.callback_wakeup_trigger, "sensor.the_cube_action", new = "shake")
        self.listen_state(self.callback_turn_on_cube, "input_boolean.the_cube", new = "on")
        self.listen_state(self.callback_turn_off_cube, "input_boolean.the_cube", new = "off")
    
    def callback_wakeup_trigger(self, entity, attribute, old, new, kwargs):
        #self.log("callback_wakeup_trigger")
        self.call_service("input_boolean/turn_on", entity_id = "input_boolean.the_cube")
    
    def callback_turn_on_cube(self, entity, attribute, old, new, kwargs):
        #self.log("callback_turn_on_cube")
        self.global_handles.append(self.listen_state(self.callback_sleep_trigger, "sensor.the_cube_action", new = "", duration = "30" , immediate = True))
        self.global_handles.append(self.listen_state(self.callback_mode_change_trigger, "sensor.the_cube_action", new = "fall"))
        self.global_handles.append(self.listen_state(self.callback_mode_change, "input_select.the_cube_modes", immediate = True))
        
    def callback_turn_off_cube(self, entity, attribute, old, new, kwargs):
        #self.log("callback_turn_off_cube")
        self.cancel_global_handles()
        self.cancel_current_mode_handles()
        self.call_service("input_select/select_first", entity_id = "input_select.the_cube_modes")
    
    def callback_sleep_trigger(self, entity, attribute, old, new, kwargs):
        #self.log("callback_sleep_trigger")
        self.call_service("input_boolean/turn_off", entity_id = "input_boolean.the_cube")

    def callback_mode_change_trigger(self, entity, attribute, old, new, kwargs):
        #self.log("callback_mode_change_trigger")
        self.call_service("input_select/select_next", entity_id = "input_select.the_cube_modes")
    
    def callback_mode_change(self, entity, attribute, old, new, kwargs):
        #self.log("callback_mode_change")
        self.cancel_current_mode_handles()
        if new == "light":
            current_side = self.get_state("sensor.the_cube_action" , attribute = "side")
            self.change_the_cube_light_rooms(current_side)
            self.mode_handles.append(self.listen_state(self.callback_change_light, "input_select.the_cube_light_rooms", immediate = True))
            self.mode_handles.append(self.listen_state(self.callback_light_knock, "sensor.the_cube_action", new = "tap"))
            self.mode_handles.append(self.listen_state(self.callback_light_rotate_right, "sensor.the_cube_action", new = "rotate_right"))
            self.mode_handles.append(self.listen_state(self.callback_light_rotate_left, "sensor.the_cube_action", new = "rotate_left"))
            self.mode_handles.append(self.listen_state(self.callback_light_filp, "sensor.the_cube_action", new = "flip90"))
            self.mode_handles.append(self.listen_state(self.callback_light_filp, "sensor.the_cube_action", new = "flip180"))
            self.mode_handles.append(self.listen_state(self.callback_light_slide, "sensor.the_cube_action", new = "slide"))
            

        if new == "cover":
            self.mode_handles.append(self.listen_state(self.callback_cover_knock, "sensor.the_cube_action", new = "tap"))
            self.mode_handles.append(self.listen_state(self.callback_cover_rotate_right, "sensor.the_cube_action", new = "rotate_right"))
            self.mode_handles.append(self.listen_state(self.callback_cover_rotate_left, "sensor.the_cube_action", new = "rotate_left"))
        
        if new == "vacuum":
            current_side = self.get_state("sensor.the_cube_action" , attribute = "side")
            self.change_the_cube_vacuums(current_side)
            self.mode_handles.append(self.listen_state(self.callback_change_vacuum, "input_select.the_cube_vacuums", immediate = True))
            self.mode_handles.append(self.listen_state(self.callback_vacuum_knock, "sensor.the_cube_action", new = "tap"))
            self.mode_handles.append(self.listen_state(self.callback_vacuum_slide, "sensor.the_cube_action", new = "slide"))
            self.mode_handles.append(self.listen_state(self.callback_vacuum_filp, "sensor.the_cube_action", new = "flip90"))
            self.mode_handles.append(self.listen_state(self.callback_vacuum_filp, "sensor.the_cube_action", new = "flip180"))
        
        if new == "tv":
            current_side = self.get_state("sensor.the_cube_action" , attribute = "side")
            self.change_the_cube_tv_sources(current_side)
            self.mode_handles.append(self.listen_state(self.callback_change_tv_sources, "input_select.the_cube_tv_sources", immediate = True))
            self.mode_handles.append(self.listen_state(self.callback_tv_knock, "sensor.the_cube_action", new = "tap"))
            self.mode_handles.append(self.listen_state(self.callback_tv_slide, "sensor.the_cube_action", new = "slide"))
            self.mode_handles.append(self.listen_state(self.callback_tv_filp, "sensor.the_cube_action", new = "flip90"))
            self.mode_handles.append(self.listen_state(self.callback_tv_filp, "sensor.the_cube_action", new = "flip180"))
            self.mode_handles.append(self.listen_state(self.callback_tv_rotate_right, "sensor.the_cube_action", new = "rotate_right"))
            self.mode_handles.append(self.listen_state(self.callback_tv_rotate_left, "sensor.the_cube_action", new = "rotate_left"))
            



    
    def cancel_current_mode_handles(self):
        #self.log("cancel_current_mode_handles")
        while len(self.mode_handles) >= 1:
            handle = self.mode_handles.pop()
            self.cancel_listen_state(handle)
    
    def cancel_global_handles(self):
        #self.log("cancel_global_handles")
        while len(self.global_handles) >= 1:
            handle = self.global_handles.pop()
            self.cancel_listen_state(handle)
    

    # LIGHTS 
    def callback_light_knock(self, entity, attribute, old, new, kwargs):
        #self.log("callback_light_knock")
        self.call_service("light/toggle" , entity_id = self.current_light, brightness_pct = 100)

    def callback_light_rotate_right(self, entity, attribute, old, new, kwargs):
        #self.log("callback_light_rotate_right")
        current_brightness = self.get_state(self.current_light, attribute = "brightness")
        if current_brightness == None:
            current_brightness = 0
        target_brightness = min(255, int(current_brightness) + 64)
        self.call_service("light/turn_on" , entity_id = self.current_light, brightness = target_brightness)

    def callback_light_rotate_left(self, entity, attribute, old, new, kwargs):
        #self.log("callback_light_rotate_left")
        self.call_service("light/toggle" , entity_id = self.current_light)
        current_brightness = self.get_state(self.current_light, attribute = "brightness")
        if current_brightness == None:
            current_brightness = 0
        target_brightness = max(0, int(current_brightness) - 64)
        self.call_service("light/turn_on" , entity_id = self.current_light, brightness = target_brightness)

    def callback_light_slide(self, entity, attribute, old, new, kwargs):
        #self.log("callback_light_slide")
        self.call_service("light/toggle" , entity_id = "light.all_lights", brightness_pct = 100)
    
    def callback_light_filp(self, entity, attribute, old, new, kwargs):
        #self.log("callback_light_filp")
        current_side = self.get_state(entity , attribute = "side")
        self.change_the_cube_light_rooms(current_side)

    def callback_change_light(self, entity, attribute, old, new, kwargs):
        #self.log("callback_change_light")
        if new == "Bureau":
            self.current_light = "light.bureau"
        if new == "Salon":
            self.current_light = "light.salon"
        if new == "Cuisine":
            self.current_light = "light.cuisine"
        if new == "Entrée":
            self.current_light = "light.entree"
        if new == "Chambre":
            self.current_light = "light.chambre"
        if new == "Extérieur":
            self.current_light = "light.exterieur"

    def change_the_cube_light_rooms(self, side):
        #self.log("change_the_cube_light_rooms")
        if side == 0:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_light_rooms" , option = "Bureau")
        if side == 1:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_light_rooms" , option = "Salon")
        if side == 2:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_light_rooms" , option = "Cuisine")
        if side == 3:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_light_rooms" , option = "Entrée")
        if side == 4:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_light_rooms" , option = "Chambre")
        if side == 5:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_light_rooms" , option = "Extérieur")
    
    # COVER
    def callback_cover_knock(self, entity, attribute, old, new, kwargs):
        #self.log("callback_cover_knock")
        self.call_service("cover/stop_cover", entity_id = "cover.living_room_cover")
    
    def callback_cover_rotate_right(self, entity, attribute, old, new, kwargs):
        #self.log("callback_cover_rotate_right")
        self.call_service("cover/open_cover", entity_id = "cover.living_room_cover")
        
    
    def callback_cover_rotate_left(self, entity, attribute, old, new, kwargs):
        #self.log("callback_cover_rotate_left")
        self.call_service("cover/close_cover", entity_id = "cover.living_room_cover")
    
    # VACUUM
    def change_the_cube_vacuums(self, side):
        #self.log("change_the_cube_vacuums")
        if side == 0:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_vacuums" , option = "NeuNeu")
        if side == 1:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_vacuums" , option = "TeuTeu")
        if side == 2:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_vacuums" , option = "NeuNeu")
        if side == 3:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_vacuums" , option = "TeuTeu")
        if side == 4:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_vacuums" , option = "NeuNeu")
        if side == 5:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_vacuums" , option = "TeuTeu")

    def callback_change_vacuum(self, entity, attribute, old, new, kwargs):
        #self.log("callback_change_vacuum")
        if new == "TeuTeu":
            self.current_vacuum = "vacuum.teuteu"
        if new == "NeuNeu":
            self.current_vacuum = "vacuum.neuneu"
    
    def callback_vacuum_filp(self, entity, attribute, old, new, kwargs):
        #self.log("callback_vacuum_filp")
        current_side = self.get_state(entity , attribute = "side")
        self.change_the_cube_vacuums(current_side)

    def callback_vacuum_knock(self, entity, attribute, old, new, kwargs):
        #self.log("callback_vacuum_knock")
        self.call_service("vacuum/start" , entity_id = self.current_vacuum)

            
        
    def callback_vacuum_slide(self, entity, attribute, old, new, kwargs):
        #self.log("callback_vacuum_slide")
        self.call_service("vacuum/return_to_base" , entity_id = self.current_vacuum)

    # TV
    def change_the_cube_tv_sources(self, side):
        #self.log("change_the_cube_tv_sources")
        if side == 0:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_tv_sources" , option = "YouTube")
        if side == 1:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_tv_sources" , option = "Plex")
        if side == 2:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_tv_sources" , option = "Netflix")
        if side == 3:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_tv_sources" , option = "Tidal")
        if side == 4:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_tv_sources" , option = "Molotov")
        if side == 5:
            self.call_service("input_select/select_option", entity_id = "input_select.the_cube_tv_sources" , option = "Amazon Prime")

    def callback_change_tv_sources(self, entity, attribute, old, new, kwargs):
        #self.log("callback_change_tv_sources")
        if new == "YouTube":
            self.current_tv_source = "YouTube"
        if new == "Plex":
            self.current_tv_source = "Plex"
        if new == "Netflix":
            self.current_tv_source = "Netflix"
        if new == "Tidal":
            self.current_tv_source = "com.aspiro.tidal"
        if new == "Molotov":
            self.current_tv_source = "Molotov"
        if new == "Amazon Prime":
            self.current_tv_source = "Prime Video"
    
    def callback_tv_filp(self, entity, attribute, old, new, kwargs):
        #self.log("callback_tv_filp")
        current_side = self.get_state(entity , attribute = "side")
        self.change_the_cube_tv_sources(current_side)
    
    def callback_tv_knock(self, entity, attribute, old, new, kwargs):
        #self.log("callback_tv_knock")
        if self.get_state("switch.media_center") == "on":
            self.call_service("media_player/media_play_pause", entity_id = "media_player.philips_android_tv")
        else:
            self.call_service("switch/turn_on", entity_id = "switch.media_center")
    
    def callback_tv_slide(self, entity, attribute, old, new, kwargs):
        #self.log("callback_tv_slide")
        self.call_service("media_player/select_source", entity_id = "media_player.philips_android_tv", source = self.current_tv_source)
    
    def callback_tv_rotate_left(self, entity, attribute, old, new, kwargs):
        #self.log("callback_tv_rotate_left")
        self.call_service("media_player/volume_down", entity_id = "media_player.lsx")
    
    def callback_tv_rotate_right(self, entity, attribute, old, new, kwargs):
        #self.log("callback_tv_rotate_right")
        self.call_service("media_player/volume_up", entity_id = "media_player.lsx")
