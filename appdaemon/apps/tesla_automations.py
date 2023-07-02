import hassapi as hass
import json
import datetime

"""
This app is responsible of all the automation related to my tesla.
Functionality : 
. Pack location update (Latitude + Longitude) to brodcast the update to MQTT so that it is integrated via mqtt.device_tracker.
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