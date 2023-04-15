import hassapi as hass

"""
clean_cat_litter_box is an app responsible of helping us clean out cat's litter box

Functionalities :
. None
Notifications :
. Cat Litter full > Cleaning possible

"""
class clean_cat_litter_box(hass.Hass): 
    def initialize(self):
        self.listen_state(self.callback_litter_occupancy_detected, "binary_sensor.capteur_mouvement_litiere" , new = "on")
        self.listen_state(self.callback_litter_full, "binary_sensor.is_litter_full", new = "on")
        self.listen_event(self.callback_button_clicked_reset_litter_tracking, "mobile_app_notification_action", action = "reset_litter_tracking")

    """
    Callback triggered when litter occupancy is detected
    Goals :
    . Increase litter tracking
    """
    def callback_litter_occupancy_detected(self, entity, attribute, old, new, kwargs):
        self.log("Occupancy detected in the litter. Incrementing litter tracking...")
        self.call_service("input_number/increment", entity_id = "input_number.litter_tracking")

    """
    Callback triggered when litter is full
    Goals :
    . notify is litter is full
    """
    def callback_litter_full(self, entity, attribute, old, new, kwargs):
        self.log("Litter full. notifying it ...")
        self.fire_event("NOTIFIER",
            action = "send_when_present",
            title = "🐈  Litière",
            message = "Penser a nettoyer la litière !",
            callback = [{
            "title" : "Litière Nettoyée",
            "event" : "reset_litter_tracking"}],
            icon =  "mdi:cat",
            color = "#ff6e07",
            persistent = True,
            tag = "litter_full",
            until =  [{
            "entity_id" : "binary_sensor.is_litter_full",
            "new_state" : "off"}])

    """
    Callback triggered when button "reset_litter_tracking" is clicked from a notification
    Goals :
    . Reset Littter Tracking
    """
    def callback_button_clicked_reset_litter_tracking(self, event_name, data, kwargs):
        self.log("Notification button clicked : Resseting Litter Tracking")
        self.call_service("input_number/set_value" , entity_id = "input_number.litter_tracking", value = 0)