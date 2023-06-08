import hassapi as hass
import datetime

"""
smart_irrigation 
"""
class smart_irrigation(hass.Hass): 
    def initialize(self):
        self.scheduler_handles = []
        self.listen_state(self.callback_irrigation_started, "switch.irrigation_switch", new = "on")
        self.listen_state(self.callback_irrigation_end_time_updated, "input_datetime.end_of_irrigation", immediate = True)
        self.listen_state(self.callback_irrigation_stopped, "switch.irrigation_switch", new = "off")
    
    def callback_irrigation_started(self, entity, attribute, old, new, kwargs):
        self.log("Irrigation started... Computing end of irrigation time")
        now = self.get_now_ts()
        irrigation_endtime = now + datetime.timedelta(minutes = float(self.entities.input_number.irrigation_time.state)).total_seconds()
        self.call_service("input_datetime/set_datetime", entity_id = "input_datetime.end_of_irrigation", timestamp = irrigation_endtime)

    def callback_irrigation_end_time_updated(self, entity, attribute, old, new, kwargs):
        self.reset_timer()
        planned_end_of_irrigation_time = self.parse_datetime(new) 
        if self.datetime() < planned_end_of_irrigation_time:
            self.log("The irrigation will end at " + str(planned_end_of_irrigation_time))
            self.scheduler_handles.append(self.run_at(self.callback_irrigation_end_time_reached, planned_end_of_irrigation_time))
        else:
            if self.entities.switch.irrigation_switch.state == "on":
                self.log("Inconsistent state... Ending Irrigation now")
                self.call_service("switch/turn_off", entity_id = "switch.irrigation_switch")

    def callback_irrigation_stopped(self, entity, attribute, old, new, kwargs):
        self.reset_timer()

    def callback_irrigation_end_time_reached(self, kwargs):
        self.log("End of irrigation reached. Stopping irrigation ...")
        self.call_service("switch/turn_off", entity_id = "switch.irrigation_switch")

    def reset_timer(self):
        self.log("Resseting timers ...")
        while len(self.scheduler_handles) >=1:
            handle = self.scheduler_handles.pop()
            self.cancel_timer(handle, silent = True)