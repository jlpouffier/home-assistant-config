import hassapi as hass
import math

"""

Grammar : 
action: notify_jl
label: lights_still_on
title: TITLE
message: MESSAGE
callback:
  - title: TITLE
    event: CALLBACK_EVENT
  - title: TITLE2
    event: CALLBACK_EVENT2
timeout: 1800
image_url: url
click_url: url
icon: mdi:icon
color: color

"""
class notifier(hass.Hass): 
    def initialize(self):
        # Listen to all NOTIFIER events
        self.listen_event(self.callback_notifier_called , "NOTIFIER")
        
        self.staged_notifications = []
        self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" , old = "off" , new = "on")

        # log
        self.log("Notifier initialized")  

    def callback_notifier_called(self, event_name, data, kwargs):
        self.log("NOTIFIER event received")  
        
        if "action" in data:
            action = data["action"] 
            if action == "sent_to_jl":
                # send_to_jl
                self.send_to_jl(data)
            elif action == "send_to_valentine":
                #send_to_valentine
                self.send_to_valetnine(data)
            elif action == "send_to_present":
                #send_to_present
                self.send_to_present(data)
            elif action == "send_to_nearest":
                #send_to_nearest
                self.send_to_nearest(data)
            elif action == "send_when_present":
                #send_when_present
                self.send_when_present(data) 
            else: 
                #send_to_jl
                self.send_to_jl(data)
        else: 
            #send_to_jl
            self.send_to_jl(data)
        
        
    def build_notification_data(self, data):
        notification_data = {}
        if "callback" in data:
            notification_data["actions"] = []
            for callback in data["callback"]:
                action = {
                    "action":callback["event"],
                    "title":callback["title"]
                }
                notification_data["actions"].append(action)

        if "timeout" in data:
            notification_data["timeout"] = data["timeout"]
        
        if "click_url" in data:
            notification_data["clickAction"] = data["click_url"]
        
        if "image_url" in data:
            notification_data["image"] = data["image_url"]

        if "icon" in data:
            notification_data["notification_icon"] = data["icon"]
        
        if "color" in data:
            notification_data["color"] = data["color"]
        
        return notification_data
    
    def send_to_jl(self, data):
        self.log("Sending notification to JL ...")
        notification_data = self.build_notification_data(data)
        self.call_service("notify/mobile_app_pixel_6", title = data["title"], message = data["message"], data = notification_data)
    
    def send_to_valetnine(self, data):
        self.log("Sending notification to Valetine ...")
        notification_data = self.build_notification_data(data)
        self.call_service("notify/mobile_app_pixel_4a", title = data["title"], message = data["message"], data = notification_data)
    
    def send_to_present(self, data):
        proximity_threshold = 1
        number_of_notification_sent = 0
        if self.get_state("person.valentine") == "home" or int(self.get_state("proximity.distance_valentine_home")) <= proximity_threshold:
            self.send_to_valetnine(data)
            number_of_notification_sent += 1
        if self.get_state("person.jenova70") == "home" or int(self.get_state("proximity.distance_jl_home")) <= proximity_threshold:
            self.send_to_jl(data)
            number_of_notification_sent +=1
        if number_of_notification_sent == 0:
            self.send_to_jl(data)
        
    def send_to_nearest(self, data):
        jl_proximity = int(self.get_state("proximity.distance_jl_home"))
        valentine_proximity = int(self.get_state("proximity.distance_valentine_home"))
        proximity_threshold = 1
        
        if math.fabs(jl_proximity - valentine_proximity) <= proximity_threshold:
            self.send_to_jl(data)
            self.send_to_valetnine(data)
        
        elif jl_proximity < valentine_proximity:
            self.send_to_jl(data)
        
        elif valentine_proximity < jl_proximity:
            self.send_to_valetnine(data)
    
    def send_when_present(self, data):
        if self.get_state("binary_sensor.home_occupied") == "on":
            self.send_to_present(data)
        else:
            self.log("Staging notification for when home becomes occupied ...")
            self.staged_notifications.append(data)
    
    def callback_home_occupied(self, entity, attribute, old, new, kwargs):
        self.log("Home is occupied ... Checking if we need to send some notification now ...")
        while len(self.staged_notifications) >= 1:
            current_data = self.staged_notifications.pop(0)
            self.send_to_present(current_data)
