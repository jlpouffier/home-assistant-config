import hassapi as hass

"""
take_out_trash is an app responsible of helping us take out our trash on time

Functionalities :
. None

Notifications :
. Take out trash

"""
class take_out_trash(hass.Hass): 
    def initialize(self):
        self.listen_state(self.callback_black_trash_schedule_begining, "schedule.planning_poubelle_noire", new = "on")
        self.listen_state(self.callback_green_trash_schedule_begining, "schedule.planning_poubelle_verte", new = "on")
        self.listen_state(self.callback_black_trash_schedule_end, "schedule.planning_poubelle_noire", new = "off")
        self.listen_state(self.callback_green_trash_schedule_end, "schedule.planning_poubelle_verte", new = "off")

    """
    Callback triggered when black trash can be taken out
    Goals :
    . Turn on input boolean to notify user on Home Assistant dashboard
    """
    def callback_black_trash_schedule_begining(self, entity, attribute, old, new, kwargs):
        self.log("It's time to take out black trash, turning on input boolean so it can be displayed on the dashboards ...")
        self.call_service("input_boolean/turn_on", entity_id = "input_boolean.poubelle_noire_a_sortir")
    
    """
    Callback triggered when green trash can be taken out
    Goals :
    . Turn on input boolean to notify user on Home Assistant dashboard
    """
    def callback_green_trash_schedule_begining(self, entity, attribute, old, new, kwargs):
        self.log("It's time to take out green trash, turning on input boolean so it can be displayed on the dashboards ...")
        self.call_service("input_boolean/turn_on", entity_id = "input_boolean.poubelle_verte_a_sortir")

    """
    Callback triggered when it's almost too late to take out black trash (and it's not yet done)
    Goals :
    . Notify present occupants
    """
    def callback_black_trash_schedule_end(self, entity, attribute, old, new, kwargs):
        if self.entities.input_boolean.poubelle_noire_a_sortir.state == "on":
            self.log("Black trash has not been taken out. Notifying it ...'")
            self.call_service("input_boolean/turn_off", entity_id = "input_boolean.poubelle_noire_a_sortir")
            self.fire_event("NOTIFIER",
                action = "send_to_present",
                title = "🗑 Poubelle Noire", 
                message = "N'oublie pas de sortir la poubelle noire",
                icon =  "mdi:delete",
                color = "deep-orange",
                tag = "black_trash")

    """
    Callback triggered when it's almost too late to take out green trash (and it's not yet done)
    Goals :
    . Notify present occupants
    """
    def callback_green_trash_schedule_end(self, entity, attribute, old, new, kwargs):
        if self.entities.input_boolean.poubelle_verte_a_sortir.state == "on":
            self.log("Green trash has not been taken out. notifying it ...'")
            self.call_service("input_boolean/turn_off", entity_id = "input_boolean.poubelle_verte_a_sortir")
            self.fire_event("NOTIFIER",
                action = "send_to_present",
                title = "♻️ Poubelle Verte", 
                message = "N'oublie pas de sortir la poubelle verte",
                icon =  "mdi:recycle",
                color = "deep-orange",
                tag = "green_trash")