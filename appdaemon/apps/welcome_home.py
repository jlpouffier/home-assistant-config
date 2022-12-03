import hassapi as hass

"""
welcome_home is an app responsible of turning on lights when we arrive at home
Functionality :
. Turn on the light everytime we get home, only if its dark, only once everytime we come back home.
"""
class welcome_home(hass.Hass):
    def initialize(self):
        self.state_handles = []
        self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" , old = "off" , new = "on")
        self.listen_state(self.callback_home_empty , "binary_sensor.home_occupied" , old = "on" , new = "off")
        self.listen_state(self.callback_home_occupied_for_more_than_x , "binary_sensor.home_occupied" , old = "off" , new = "on" , duration = 900)
        self.log("Initialized")
    
    def callback_home_occupied(self, entity, attribute, old, new, kwargs):
        if len(self.state_handles) < 1:
            self.state_handles.append(self.listen_state(self.callback_entry_door_open , "binary_sensor.capteur_ouverture_porte_entree" , old = "off" , new = "on"))
    
    def callback_home_empty(self, entity, attribute, old, new, kwargs):
        self.cancel_callback()

    def callback_home_occupied_for_more_than_x(self, entity, attribute, old, new, kwargs):
        self.cancel_callback()
    
    def callback_entry_door_open(self, entity, attribute, old, new, kwargs):
        if self.get_state("sun.sun") == "below_horizon":
            # Home occupied for less than 15 minutes + Entry door open + Sun below horizon = Welcome home
            self.log("Home occupied for less than 15 minutes + Entry door open + Sun below horizon : Welcome Home!")
            sequence = [
                {
                    "hue/activate_scene":{
                        "entity_id":"scene.entree_entree_100",
                        "transition":3
                    }
                },
                {
                    "sleep":3
                },
                {
                    "hue/activate_scene":{
                        "entity_id":"scene.salon_salon_100",
                        "transition":3
                    }
                },
                {
                    "sleep":3
                },
                {
                    "hue/activate_scene":{
                        "entity_id":"scene.cuisine_cuisine_100",
                        "transition":3
                    }
                }
            ]
            self.run_sequence(sequence)
            self.cancel_callback()

        
    def cancel_callback(self):
        while len(self.state_handles) >=1:
            handle = self.state_handles.pop()
            self.cancel_listen_state(handle)
