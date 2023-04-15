import hassapi as hass

"""
handle_cover_edge_cases is an app responsible of handing desynchronization edge case with my living room cover 

Functionalities :
. Deal with desynchronization edge case with my living room cover

Notifications :
. None

"""

class handle_cover_edge_cases(hass.Hass): 
    def initialize(self):
        self.listen_event(self.callback_cover_open_service_called, "call_service", domain = "cover", service = "open_cover" , service_data = {"entity_id" : "cover.living_room_cover"})
        self.listen_event(self.callback_cover_close_service_called, "call_service", domain = "cover", service = "close_cover" , service_data = {"entity_id" : "cover.living_room_cover"})
    
    """
    Callback triggered when the service open_cover is called on cover.living_room_cover
    Goals :
    . If the over are already fully opened, press again the open button to tackle edge case of desynchronization between the different remotes.
    """
    def callback_cover_open_service_called(self, event_name, data, kwargs):
        if self.entities.cover.living_room_cover.state == "open" and self.entities.cover.living_room_cover.attributes.current_position == 100:
            self.log("Action open cover fired, but cover already opened at 100%: Making sure they are opened")
            self.call_service("switch/turn_on" , entity_id = "switch.volet_salon_bouton_up_fallback")

    """
    Callback triggered when the service close_cover is called on cover.living_room_cover
    Goals :
    . If the over are already fully closed, press again the close button to tackle edge case of desynchronization between the different remotes.
    """
    def callback_cover_close_service_called(self, event_name, data, kwargs):
        if self.entities.cover.living_room_cover.state == "closed" and self.entities.cover.living_room_cover.attributes.current_position == 0:
            self.log("Action close cover fired, but cover already closed at 0%: Making sure they are closed")
            self.call_service("switch/turn_on" , entity_id = "switch.volet_salon_bouton_down_fallback")