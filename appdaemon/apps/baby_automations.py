import hassapi as hass
import datetime

"""
baby_automations is an app responsible of helping us to know when to give the next baby bottle to our daugther. It also sync the only non-hue light we have in her bedroom.

Functionalities :
    Store the last feeding time into input_datetime.dernier_bibi
    Sync the miffy light to other light in the bedroom

Notifications :
    Minimum feeding time reached
    Optimal feeding time reached
    Maximum feeding time reached
"""
class baby_automations(hass.Hass):
    def initialize(self):
        self.bibi_scheduler_handles = []
        self.listen_state(self.callback_bouton_bibi_pressed, "sensor.bouton_bibi_action", new = "press")
        self.listen_state(self.callback_last_bibi_timestamp_updated, "input_datetime.dernier_bibi", immediate = True)
        self.listen_state(self.callback_light_on, "light.chambre_bebe_suspension", new = "on")
        self.listen_state(self.callback_light_off, "light.chambre_bebe_suspension", new = "off")
        self.listen_state(self.callback_brightness_updated, "light.chambre_bebe_suspension", attribute = "brightness")
                
        self.log("Initialized")

    '''
    Callback trigerred when the feeding button is pressed
    Goals :
        Update the feeding time stored on input_datetime.dernier_bibi
    '''
    def callback_bouton_bibi_pressed(self, entity, attribute, old, new, kwargs):
        self.log("Bibi Button Pressed ... Changing Last feeding timestamp")
        self.call_service("input_datetime/set_datetime", entity_id = "input_datetime.dernier_bibi", timestamp = self.get_now_ts())

    '''
    Callback trigerred when the feeding time (input_datetime.dernier_bibi) is updated
    Goals :
        Deregister old callbacks
        Register new callbacks
    '''
    def callback_last_bibi_timestamp_updated(self, entity, attribute, old, new, kwargs):
        self.log("Last feeding timestamp updated ... registering callbacks for future notifications ...")

        while len(self.bibi_scheduler_handles) >=1:
            handle = self.bibi_scheduler_handles.pop()
            self.cancel_timer(handle, silent = True)
        
        self.fire_event("NOTIFIER_DISCARD", tag = "baby_bottle")
        
        last_bibi_date_time = self.parse_datetime(new)
        next_bibi_minimum_date_time = last_bibi_date_time + datetime.timedelta(hours = self.args["minimum_delay_between_bibi_in_hours"]) 
        next_bibi_optimal_date_time = last_bibi_date_time + datetime.timedelta(hours = self.args["optimal_delay_between_bibi_in_hours"]) 
        next_bibi_maximum_date_time = last_bibi_date_time + datetime.timedelta(hours = self.args["maximum_delay_between_bibi_in_hours"]) 
        
        if self.datetime() < next_bibi_minimum_date_time:
            self.log("Minimum feeding time registered for " + str(next_bibi_minimum_date_time))
            self.bibi_scheduler_handles.append(self.run_at(self.callback_next_bibi_possible, next_bibi_minimum_date_time))
        if self.datetime() < next_bibi_optimal_date_time:
            self.log("Optimal feeding time registered for " + str(next_bibi_optimal_date_time))
            self.bibi_scheduler_handles.append(self.run_at(self.callback_next_bibi_optimal, next_bibi_optimal_date_time))
        if self.datetime() < next_bibi_maximum_date_time:
            self.log("Maximum feeding time registered for " + str(next_bibi_maximum_date_time))
            self.bibi_scheduler_handles.append(self.run_at(self.callback_next_bibi_needed, next_bibi_maximum_date_time))   

    '''
    Callback trigerred when the Minimum feeding time is reached
    Goals : 
        Notify
    '''
    def callback_next_bibi_possible(self, kwargs):
        self.log("Minimum feeding time reached... Sending Notification ...")
        self.fire_event("NOTIFIER",
            action = "send_to_all",
            title = "🧸 " + self.args["kid_name"], 
            message = self.args["kid_name"] + " a pris son bibi il y a 2 heures, prochain Bibi possible",
            click_url="dashboard-baby/baby",
            icon =  "mdi:baby-bottle-outline",
            color = "light-blue",
            tag = "baby_bottle")

    '''
    Callback trigerred when the Optimal feeding time is reached
    Goals :
        Notify
    '''
    def callback_next_bibi_optimal(self, kwargs):
        self.log("Optimal feeding time reached... Sending Notification ...")
        self.fire_event("NOTIFIER",
            action = "send_to_all",
            title = "🧸 " + self.args["kid_name"],  
            message = self.args["kid_name"] + " a pris son bibi il y a 4 heures, prochain Bibi recommandé",
            click_url="dashboard-baby/baby",
            icon =  "mdi:baby-bottle",
            color = "green",
            tag = "baby_bottle")

    '''
    Callback trigerred when the Maximum feeding time is reached
    Goals : 
        Notify
    '''
    def callback_next_bibi_needed(self, kwargs):
        self.log("Maximum feeding time reached... Sending Notification ...")
        self.fire_event("NOTIFIER",
            action = "send_to_all",
            title = "🧸 " + self.args["kid_name"],  
            message = self.args["kid_name"] + " a pris son bibi il y a 6 heures, prochain Bibi nécessaire",
            click_url="dashboard-baby/baby",
            icon =  "mdi:baby-bottle",
            color = "deep-orange",
            tag = "baby_bottle")
    
    def callback_light_on(self, entity, attribute, old, new, kwargs):
        try:
            target_brightness = self.entities.light.chambre_bebe_suspension.attribute.brightness
        except:
            target_brightness = 100
        self.call_service("light/turn_on", entity_id = "light.miffy", brightness = target_brightness)
    
    def callback_light_off(self, entity, attribute, old, new, kwargs):
        self.call_service("light/turn_off", entity_id = "light.miffy")
    
    
    def callback_brightness_updated(self, entity, attribute, old, new, kwargs):
        self.call_service("light/turn_on", entity_id = "light.miffy", brightness = new)
    
    
    