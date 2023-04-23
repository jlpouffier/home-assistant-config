import hassapi as hass
import datetime

"""
heat_home is an app responsible of driving the home thermostat to reduce energy loss

Functionalities :
    Frost guard if windows / doors opened for too long
    Turn on again thermostat if stopped by windows / doors opened for too long
"""
class heat_home(hass.Hass): 
    def initialize(self):
        self.listen_state(self.callback_conditions_changed, ["binary_sensor.is_home_open_since_more_than_one_minute", "binary_sensor.home_occupied"], immediate = True)
        self.listen_state(self.callback_heating_schedule_selector_updated, "input_select.heating_schedule_selector", immediate = True)
        time = datetime.time(0, 0, 0)
        self.run_minutely(self.callback_check_temperature_coherency, time)

    """
    Callback triggered when    
        window / door opened or for too long.
        home becomes occupied or not
    Goals :
        Change Heating Schedule Selector
    """
    def callback_conditions_changed(self, entity, attribute, old, new, kwargs):
        if self.entities.binary_sensor.is_home_open_since_more_than_one_minute.state == "on":
            self.log("Window or door opened ... Setting the thermostat mode to Frost Guard.")
            self.call_service("input_select/select_option", entity_id = "input_select.heating_schedule_selector", option = "Frost Guard")
        elif self.entities.binary_sensor.home_occupied.state == "on":
            self.log("Home occupied: Setting the thermostat mode to Present")
            self.call_service("input_select/select_option", entity_id = "input_select.heating_schedule_selector", option = "Présent")
        elif self.entities.binary_sensor.home_occupied.state == "off":
            self.log("Home empty: Setting the thermostat mode to Away")
            self.call_service("input_select/select_option", entity_id = "input_select.heating_schedule_selector", option = "Absent")
        

    """
    Callback triggered Heating Schedule Selector changes
    Goals :
        compute the target temperature
        compare it the the current target temperature
        change it if needed
    """
    def callback_heating_schedule_selector_updated(self, entity, attribute, old, new, kwargs):
        target_temperature = self.set_target_temperature()
        current_temperature = int(self.entities.climate.netatmo.attributes.temperature)

        if target_temperature != current_temperature:
            self.log("Mode changed ... Changing temperature")
            self.call_service("climate/set_temperature", entity_id = "climate.netatmo", temperature = target_temperature)
    
    """
    Callback triggered every minute
    Goals :
        compute the target temperature
        compare it the the current target temperature
        change it if needed
    """
    def callback_check_temperature_coherency(self, kwargs):
        target_temperature = self.set_target_temperature()
        current_temperature = int(self.entities.climate.netatmo.attributes.temperature)

        if target_temperature != current_temperature:
            self.log("Temperature not coherent ... Changing temperature")
            self.call_service("climate/set_temperature", entity_id = "climate.netatmo", temperature = target_temperature)

    """
    Helper method:
    Does : 
        nothing
    Returns : 
        The target temperature right now based on the Heating Schedule Selector and the calendar entities.
    """
    def set_target_temperature(self):
        if self.entities.input_select.heating_schedule_selector.state == "Présent":
            target_calendar = "calendar.heating_schedule_present"
            default_temperature = 17
        elif self.entities.input_select.heating_schedule_selector.state == "Absent":
            target_calendar = "calendar.heating_schedule_absent"
            default_temperature = 16
        elif self.entities.input_select.heating_schedule_selector.state == "Frost Guard":
            target_calendar = "calendar.heating_schedule_frost_guard"
            default_temperature = 7

        if self.get_state(target_calendar) == "on":
            try:
                target_temperature = int(self.get_state(target_calendar, attribute = "message"))
            except:
                self.log("WARNING ! CALENDAR ENTRY INVALD, DEFAULTING")
                target_temperature = default_temperature
        else:
            self.log("WARNING ! CALENDAR IS OFF... IT SHOULD NOT HAPPEN, DEFAULTING")
            target_temperature = default_temperature
        
        return target_temperature
        