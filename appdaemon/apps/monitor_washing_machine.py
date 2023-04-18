import hassapi as hass

"""
monitor_washing_mashine is an app responsible of the monitoring our washing machine 

Functionalities :
. None

Notifications :
. Washing Machine over
"""

class monitor_washing_machine(hass.Hass): 
    def initialize(self):
        self.listen_state(self.callback_washing_mashine_over, "binary_sensor.is_washing_machine_running" , old = "on", new = "off")

    """
    Callback triggered when washing machine is over
    Goals :
    . Send notification
    """
    def callback_washing_mashine_over(self, entity, attribute, old, new, kwargs):
        self.log("Washing machine over. Notifying it...")
        self.fire_event("NOTIFIER",
            action = "send_when_present",
            title = "🫧 Machine à laver",
            message = "Cycle de lavage terminé !",
            icon =  "mdi:washing-machine",
            color = "green",
            tag = "washing_mashine_over")