import hassapi as hass

"""
monitor_mailbox is an app responsible of the monitoring our mailbox 

Functionalities :
. Discard Notification when taking out mail.

Notifications :
. Mailbox full

"""
class monitor_mailbox(hass.Hass): 
    def initialize(self):
        self.listen_state(self.callback_mailbox_occupancy_detected, "binary_sensor.capteur_mouvement_boite_aux_lettres" , new = "on")

    """
    Callback triggered when mailbox occupancy is detected
    Goals :
    . Send notification, not when the main door is opened (rencently)
    . Discard notification when the main door is opened (rencently)
        (that's how I pick my mail)
    """
    def callback_mailbox_occupancy_detected(self, entity, attribute, old, new, kwargs):
        # if the main door was opened recently .. send notification
        if self.entities.binary_sensor.is_front_door_recently_open.state == "off":
            self.log("Occupancy detected in the mailbox + Door not opened recently: Notifying it...")
            self.fire_event("NOTIFIER",
                action = "send_when_present",
                title = "📬  Boite aux lettres",
                message = "Vous avez du courrier !",
                icon =  "mdi:mailbox-up",
                color = "green",
                tag = "you_got_mail")
        # else discard
        else:
            self.log("Occupancy detected in the mailbox + Door opened recently: Discarding notification...")
            self.fire_event("NOTIFIER_DISCARD", tag = "you_got_mail")