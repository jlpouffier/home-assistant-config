import hassapi as hass
import datetime


"""
monitor_system is an app responsible of 

Functionalities :
. Full backup everyday at 1am

Notifications :
  . Notify update
  . Notify if RPI power is not OK
  . Notify low batteries on all battery poweered devices 

"""
class monitor_system(hass.Hass): 
    def initialize(self):
        
        # Listen to all updater state change
        self.listen_state(self.callback_update_available, "update" , new = "on" , immediate = True)

        # Listen to RPI power status
        self.listen_state(self.callback_rpi_power_problem_detected, "binary_sensor.rpi_power_status" , new = "on" , immediate = True)

        # Daily back-up
        backup_runtime = datetime.time(1,0,0)
        self.run_daily(self.callback_trigger_backup, backup_runtime)
        
        # Battery daily check
        battery_daily_check_runtime = datetime.time(19,0,0)
        self.run_daily(self.callback_battery_daily_check, battery_daily_check_runtime)

    """
    Callback triggered when new upate is available on the HASS domain.
    Goals :
    . Notify
    """
    def callback_update_available(self, entity, attribute, old, new, kwargs):
        self.log("Detecting an available update... Notifying it...")
    
        app_title = self.get_state(entity, attribute = "friendly_name")

        if app_title is not None:
            message = app_title
        else:
            message = "(Entité inconnue)"
    
        self.fire_event("NOTIFIER",
            action = "send_to_jl",
            title = "🎉 Mise a jour disponible",
            message = message,
            click_url = "/config/dashboard",
            icon = "mdi:cellphone-arrow-down",
            tag = entity,
            until =  [{
                "entity_id" : entity,
                "new_state" : "off"}])

    """
    Callback triggered when a power issue is detected on the RPI
    Goals :
    . Notify
    """
    def callback_rpi_power_problem_detected(self, entity, attribute, old, new, kwargs):
        self.log("Detecting power issue on RPI... Notifying it...")
        self.fire_event("NOTIFIER",
            action = "send_to_jl",
            title = "🔌 Alimentation Home Assistant",
            message = "Problème détecté sur l'alimentation de Home Assistant",
            icon = "mdi:power-plug",
            color = "deep-orange",
            persistent = True)


    """
    Callback triggered everyday at 1am
    Goals :
    . Full back-up
    """
    def callback_trigger_backup(self, kwargs):
        self.log("Backing-up the system ...")
        backup_time = self.get_now()
        backup_name = "Home Assistant Backup " + str(backup_time)
        self.call_service("hassio/backup_full", name = backup_name)

    """
    Callback triggered everyday at 7pm
    Goals :
    . Notify if some batteries are low
    """
    def callback_battery_daily_check(self, kwargs):
        self.log("Checking battery levels  ...")
        
        battery_threshold = self.args["battery_threshold"]
        entities_to_notify = []

        for battery_sensor in self.args["battery_sensors_to_check"]:
            try:
                battery_level = float(self.get_state(battery_sensor))
            except:
                self.log("Battery level of entity " + battery_sensor + " is not a float! Ignoring!")
                battery_level = 100
        
            if battery_level < battery_threshold:
                friendly_name = self.get_state(battery_sensor, attribute = "friendly_name")
                entities_to_notify.append(friendly_name)
            
        if len(entities_to_notify) == 1:
            self.log("Low battery... Notifying it")
            self.fire_event("NOTIFIER",
                action = "send_to_jl",
                title = "Batterie 🪫",
                message= "Pensez a changer les piles de l'appareil suivant: " + entities_to_notify[0],
                icon =  "mdi:battery-20",
                color = "deep-orange",
                persistent = True)
        
        elif len(entities_to_notify) > 1:
            self.log("Low battery... Notifying it")
            self.fire_event("NOTIFIER",
                action = "send_to_jl",
                title = "Batterie 🪫",
                message= "Pensez a changer les piles des appareils suivants: " + ", ".join(entities_to_notify),
                icon =  "mdi:battery-20",
                color = "deep-orange",
                persistent = True)