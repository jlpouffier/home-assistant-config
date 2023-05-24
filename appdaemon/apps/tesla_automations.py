import hassapi as hass
import json
import datetime

"""
This app is responsible of all the automation related to my tesla.
Functionality : 
. Pack location update (Latitude + Longitude) to brodcast the update to MQTT so that it is integrated via mqtt.device_tracker.

Notification :
. End of charge after off-peak hour.

"""

class tesla_automations(hass.Hass): 
    def initialize(self):
        self.location = {
            'latitude' : 0,
            'longitude' : 0
        }
        self.update_ts = {
            'latitude' : 0,
            'longitude' : 0
        }
        self.update_time_difference = 0

        self.listen_state(self.callback_location_updated, ['sensor.tesla_latitude','sensor.tesla_longitude'])
        self.listen_state(self.callback_tesla_charging_session_started, "sensor.tesla_state", new = "charging", duration = 60)

    """
    Callback triggered when either the latitude or the longitude of my tesla is updated
    Goals :
        Store update timestamp.
        Compare the update timestamp of the other dimension (Latitude or Longiture)
            If both update are on a short time frame: Send location update into MQTT topic tesla/location
    """
    def callback_location_updated(self, entity, attribute, old, new, kwargs):
        if entity == 'sensor.tesla_longitude' and new not in ['unavailable', 'unknown']:
            self.location['longitude'] = float(new)
            self.update_ts['longitude'] = self.get_now_ts()
        elif entity == 'sensor.tesla_latitude' and new not in ['unavailable', 'unknown']:
            self.location['latitude'] = float(new)
            self.update_ts['latitude'] = self.get_now_ts()

        self.update_time_difference = abs( self.update_ts['latitude'] - self.update_ts['longitude'] )

        if self.update_time_difference < self.args["max_delay_between_coordinate_update_to_send_location_update"]:
            self.call_service('mqtt/publish', qos = '0', retain = True, topic ='tesla/location', payload =  json.dumps(self.location))
            self.update_ts['latitude'] = 0
            self.update_ts['longitude'] = 0

    """
    Callback triggered when the tesla charges
    Goals :
        Check if tesla home
        Check if we are currently in off peak hour
        check if the charge end time will be after the end of the off-peak hour.
            Notify if all the above is true
    """
    def callback_tesla_charging_session_started(self, entity, attribute, old, new, kwargs):
        if self.entities.device_tracker.tesla_device_tracker.state == "home" and self.entities.schedule.heures_pleines.state == "off":
            
            planned_charge_end_time = self.get_now() + datetime.timedelta(hours = float(self.entities.sensor.tesla_time_to_full_charge.state))
            off_peak_end_time = self.convert_utc(self.entities.schedule.heures_pleines.attributes.next_event)
            
            # TODO: Calculate new target to include it in the notification

            if planned_charge_end_time > off_peak_end_time:
                self.log("The end of the charge will be after off peak hour... Notifying")
                self.fire_event("NOTIFIER",
                    action = "send_to_jl",
                    title = "️🚗 Tesla", 
                    message = "La recharge est prevue de finir après la fin des heures creuse (" + str(planned_charge_end_time.strftime("%H:%M")) + "). Pense à reduire la cibe de recharge",
                    click_url="/lovelace/tesla",
                    icon =  "mdi:car",
                    color = "deep-orange",
                    tag = "tesla_end_charge_after_off_peak_hours")