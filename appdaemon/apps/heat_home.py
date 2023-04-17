import hassapi as hass

"""
heat_home is an app responsible of driving the home thermostat to reduce energy loss

Functionalities :
    Turn off thermostat if windows / doors opened for too long
    Turn on again thermostat if stopped by windows / doors opened for too long
"""
class heat_home(hass.Hass): 
    def initialize(self):
        self.listen_state(self.callback_openings_open, "binary_sensor.is_home_open_since_more_than_one_minute", new = "on")
        self.listen_state(self.callback_openings_closed, "binary_sensor.is_home_open_since_more_than_one_minute", new = "off")
        self.listen_state(self.callback_home_empty, "binary_sensor.home_occupied", new= "off")
        self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" , new = "on")

    """
    Callback triggered when window / door opened for too long.
    Goals :
        Turn off thermostat
    """
    def callback_openings_open(self, entity, attribute, old, new, kwargs):
        self.log("Window or door opened ... Setting the thermostat mode to Frost Guard.")
        self.call_service("select/select_option", entity_id = "select.planning_netatmo", option = "Protection Gel 5")

    """
    Callback triggered when window / door closed
    Goals :
        Turn on thermostat 
    """
    def callback_openings_closed(self, entity, attribute, old, new, kwargs):
        if self.entities.binary_sensor.home_occupied.state == "on":
            self.log("Home occupied and closed: Setting the thermostat mode to Present")
            self.call_service("select/select_option", entity_id = "select.planning_netatmo", option = "Present")
        else:
            self.log("Home empty and closed: Setting the thermostat mode to Away")
            self.call_service("select/select_option", entity_id = "select.planning_netatmo", option = "Absent 16")

    """
    Callback triggered when home become empty
    Goals :
        Set thermostat mode to Away
    """
    def callback_home_empty(self, entity, attribute, old, new, kwargs):
        if self.entities.binary_sensor.is_home_open_since_more_than_one_minute.state == "on":
            self.log("Home empty and open: Setting the thermostat mode to Frost Guard")
            self.call_service("select/select_option", entity_id = "select.planning_netatmo", option = "Protection Gel 5")
        else:
            self.log("Home empty and closed: Setting the thermostat mode to Away")
            self.call_service("select/select_option", entity_id = "select.planning_netatmo", option = "Absent 16")

    """
    Callback triggered when home become empty
    Goals :
        Set thermostat mode to Present
    """
    def callback_home_occupied(self, entity, attribute, old, new, kwargs):
        if self.entities.binary_sensor.is_home_open_since_more_than_one_minute.state == "on":
            self.log("Home occupied and open: Setting the thermostat mode to Frost Guard")
            self.call_service("select/select_option", entity_id = "select.planning_netatmo", option = "Protection Gel 5")
        else:
            self.log("Home occupied and closed: Setting the thermostat mode to Present")
            self.call_service("select/select_option", entity_id = "select.planning_netatmo", option = "Present")

