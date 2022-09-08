import hassapi as hass
import math

"""
 
Notify is an app responsible for notifying the right occupant(s) at the right time, and making sure to discard notifications once they are not relevant anymore.
 
The complete app can be called from anywhere by sending a custom event NOTIFIER with the following grammar:
 
action: <string>
title: <string>
message: <string>
callback:
 - title: <string>
   event: <string>
 - title: <string>
   event: <string>
timeout: <number>
image_url: <url>
click_url: <url>
icon: <string>
color: <string>
tag: <string>
persistent: <boolean>
until:
 - entity_id: <string>
   new_state: <string>
 - entity_id: <string>
   new_state: <string>

Here are detialed explanation for every field:

action can be the following:
- send_to_jl: Send a notification directly to JL
- send_to_valentine: Send a notification directly to Valentine
- send_to_present: Send a notification directly to all present occupant of the home, fallback to send_to_jl in case the home is empty
- send_to_nearest: Send a notification to the nearest occupant(s) of the home
- send_when_present:
   - if the home is occupied: Send a notification directly to all present occupant of the home
   - if the home is empty: Stage the notification and send it once the home becomes occupied
If action is omitted, or if action has any other value,: fallback to send_to_jl
 
title: Title of the notification
 
message: Body of the notification
 
callback: Actionable buttons of the notification
   - title: Title of the button
   - event: a string that will be used the catch back the event when the button is pressed.
     If event: turn_off_lights, then an event "mobile_app_notification_action" with action = "turn_off_lights" will be triggered once the button is pressed.
     Up to the app / automation creating the notification to listen to this event and perform some action.
 
timeout: Timeout of the notification in seconds. timeout: 60 will display the notification for one minute, then discard it automatically.
 
image_url: url of an image that will be embedded on the notification. Useful for cameras, vacuum maps, etc.
 
click_url: url of the target location if the notification is pressed.
If you have a lovelace view called "/lovelace/vacuums" for your vacuum, then putting click_url: "/lovelace/vacuums" will lead to this view if the notification is clicked
 
icon: Icon of the notification. format mdi:<string>. Visit https://materialdesignicons.com/ for supported icons
 
color: color of the notification.
Format can be "red" or "#ff6e07"
 
tag: The concept of tag is complex to understand. So I'll explain the behavior you will experience while using tags.
  - A subsequent notification with a tag will replace an old notification with the same tag.
    For example if you want to notify that a vacuum is starting, and then finishing: use the same tag for both (like "vacuum") and the "Cleaning complete" notification will replace the "Cleaning started" notification, as it is not relevant anymore.
  - If you notify more than one person with the same tag:
    - Discarding the notification on a device will discard it on every other devices
    - Acting on the notification (a button) on a device will discard it on every other devices
    Example: If you notify all occupants that the lights are still on while the home is empty with an actionable button to turn off the lights, if person A clicks on "Turn off lights" then person B will see the notification disappear... Because it's not relevant anymore (it's done)
  - The next field "until" requires the field tag to work too (See below)

until (note: "tag" is required for "until" to work)
until dynamically creates watcher(s) to clear notification.
I prefer to explain it with an example:
If you want to notify all occupants that the lights are still on while the home is empty, you can specify
until:
 - entity_id: binary_sensor.home_occupied
   new_state : on
 - entity_id: light.all_lights
   new_state : off
This will make the notification(s) disappear as soon as the lights are off, or the home becomes occupied.
That way, you make sure notifications are only displayed when relevant.
 
"""

class notifier(hass.Hass): 
    def initialize(self):
        # Listen to all NOTIFIER events
        self.listen_event(self.callback_notifier_called , "NOTIFIER")
        self.listen_event(self.callback_button_clicked, "mobile_app_notification_action")
        self.listen_event(self.callback_notification_cleared, "mobile_app_notification_cleared")
        
        self.staged_notifications = []
        self.listen_state(self.callback_home_occupied , "binary_sensor.home_occupied" , old = "off" , new = "on")

        self.watchers_handles = []

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
        
        if "persistent" in data:
            if data["persistent"]:
                self.log("Persisting the notification on Home Assistant Front-end ...")
                self.call_service("notify/persistent_notification", title = data["title"], message = data["message"])
        
        if "until" in data and 'tag' in data:
            until = data["until"]
            for watcher in until:
                watcher_handle = {}
                watcher_handle["id"] = self.listen_state(self.callback_until_watcher, watcher["entity_id"], new = str(watcher["new_state"]), oneshot = True, tag = data["tag"])
                watcher_handle["tag"] = data["tag"]
                self.watchers_handles.append(watcher_handle)
                self.log("All notifications with tag " + data["tag"] + " will be cleared if " + watcher["entity_id"] + " transitions to " + str(watcher["new_state"]))

    def callback_until_watcher(self, entity, attribute, old, new, kwargs):
        self.clear_notifications(kwargs["tag"])

    def callback_button_clicked(self, event_name, data, kwargs):
        if "tag" in data:
            self.clear_notifications(data["tag"])

    def callback_notification_cleared(self, event_name, data, kwargs):
        if "tag" in data:
            self.clear_notifications(data["tag"])
    
    def clear_notifications(self, tag):
        self.log("Clearing notifications with tag " + tag + " (if any) ...")
        notification_data = {}
        notification_data["tag"] = tag
        self.call_service("notify/mobile_app_pixel_6", message = "clear_notification", data = notification_data)
        self.call_service("notify/mobile_app_pixel_4a", message = "clear_notification", data = notification_data)
        self.cancel_watchers(tag)

    def cancel_watchers(self, tag):
        self.log("Removing watchers with tag " + tag + " (if any) ...")
        for watcher in list(self.watchers_handles):
            if watcher["tag"] == tag:
                self.watchers_handles.remove(watcher)
        
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
        if "tag" in data:
            notification_data["tag"] = data["tag"]
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
