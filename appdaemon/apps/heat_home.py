import hassapi as hass

"""
heat_home is an app responsible of driving the home thermostat to reduce energy loss

Functionalities :
. Turn off thermostat if windows / doors opened for too long
. Turn on again thermostat if stopped by windows / doors opened for too long
"""
class heat_home(hass.Hass): 
    def initialize(self):
        self.listen_state(self.callback_doors_or_windows_open, "binary_sensor.all_doors", new = "on", duration = 60)
        self.listen_state(self.callback_doors_or_windows_open, "binary_sensor.all_windows", new = "on", duration = 60)
        self.listen_state(self.callback_doors_or_windows_closed, "binary_sensor.all_doors", new = "off")
        self.listen_state(self.callback_doors_or_windows_closed, "binary_sensor.all_windows", new = "off")
        self.log("Heat Home automations initialized")

    """
    Callback triggered when window / door opened for too long.
    Goals :
    . Turn off thermostat if heating in progress
    """
    def callback_doors_or_windows_open(self, entity, attribute, old, new, kwargs):
        if self.get_state("climate.netatmo", attribute = "hvac_action") == "heating":
            self.log("Window or door opened, and heating in progress ... stopping thermostat temporarly.")
            self.call_service("climate/turn_off", entity_id = "climate.netatmo")

    """
    Callback triggered when window / door closed
    Goals :
    . Turn on thermostat if stopped before
    """
    def callback_doors_or_windows_closed(self, entity, attribute, old, new, kwargs):
        if self.get_state("climate.netatmo") == 'off':
            self.log("Window or door closed, and thermostat stopped ... restating thermostat.")
            self.call_service("climate/turn_on", entity_id = "climate.netatmo")
