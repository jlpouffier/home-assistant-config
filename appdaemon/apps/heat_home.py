import hassapi as hass

"""
heat_home is an app responsible of driving the home thermostat to reduce energy loss

Functionalities :
. Turn off thermostat if windows / doors opened for too long
. Turn on again thermostat if stopped by windows / doors opened for too long
"""
class heat_home(hass.Hass): 
    def initialize(self):
        self.listen_state(self.callback_openings_open, "binary_sensor.all_openings", new = "on", duration = self.args["open_time_allowed_before_stopping_thermostat"])
        self.listen_state(self.callback_openings_closed, "binary_sensor.all_openings", new = "off")
        self.listen_state(self.callback_home_empty, "binary_sensor.home_occupied", new= "off")
        self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" , new = "on")

        self.log("Heat Home automations initialized")

    """
    Callback triggered when window / door opened for too long.
    Goals :
    . Turn off thermostat
    """
    def callback_openings_open(self, entity, attribute, old, new, kwargs):
        if self.get_state("climate.netatmo") != 'off':
            self.log("Window or door opened, and thermostat not stopped ... stopping thermostat temporarly.")
            self.call_service("climate/turn_off", entity_id = "climate.netatmo")

    """
    Callback triggered when window / door closed
    Goals :
    . Turn on thermostat 
    """
    def callback_openings_closed(self, entity, attribute, old, new, kwargs):
        if self.get_state("climate.netatmo") == 'off':
            self.log("Window or door closed, and thermostat stopped ... restating thermostat.")
            self.call_service("climate/turn_on", entity_id = "climate.netatmo")

    """
    Callback triggered when home become empty
    Goals :
    . set thermostat mode to Away
    """
    def callback_home_empty(self, entity, attribute, old, new, kwargs):
        self.log("Home empty: Setting the thermostat mode to Away")
        self.call_service("select/select_option", entity_id = "select.planning_netatmo", option = "Absent 16")

    """
    Callback triggered when home become empty
    Goals :
    . set thermostat mode to Present
    """
    def callback_home_occupied(self, entity, attribute, old, new, kwargs):
        self.log("Home empty: Setting the thermostat mode to Present")
        self.call_service("select/select_option", entity_id = "select.planning_netatmo", option = "Present")

