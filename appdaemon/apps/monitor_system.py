import hassapi as hass
import datetime


"""
monitor_system is an app responsible of 

Functionalities :
.

Notifications :
  . Notify HASS update
  . Notify HACS update
  . Notify if RPI power is not OK
  . Notify last back-up older than 24 hours.
  . Notify low batteries on all battery poweered devices 



"""
class monitor_system(hass.Hass): 
    def initialize(self):
        
        # Listen to all updater state change
        self.listen_state(self.callback_hass_update_available, "update" , new = "on" , immediate = True)

        # Listen to HACS pending update
        self.listen_state(self.callback_hacs_update_available, "sensor.hacs" , immediate = True)

        # Listen to RPI power status
        self.listen_state(self.callback_rpi_power_problem_detected, "binary_sensor.rpi_power_status" , new = "on" , immediate = True)

        # Samba back-up daily check
        samba_backup_daily_check_runtime = datetime.time(10,0,0)
        self.run_daily(self.callback_samba_backup_daily_check, samba_backup_daily_check_runtime)
        
        # Battery daily check
        battery_daily_check_runtime = datetime.time(19,0,0)
        self.run_daily(self.callback_battery_daily_check, battery_daily_check_runtime)
        
        self.log("Monitor System Initializing, Restauring Samba Backup sensor ...")
        self.call_service("hassio/addon_stdin", addon = "15d21743_samba_backup" , input = "restore-sensor")
        
        self.log("Initialized")

    """
    Callback triggered when new upate is available on the HASS domain.
    Goals :
    . Notify
    """
    def callback_hass_update_available(self, entity, attribute, old, new, kwargs):
        self.log("Detecting an available update... Notifying it...")
    
        app_title = self.get_state(entity, attribute = "title")
    
        self.fire_event("NOTIFIER",
            action = "send_to_jl",
            title = "🎉 Mise a jour disponible",
            message = "Une mise a jour est disponible pour " + app_title,
            click_url = "/config/dashboard",
            icon = "mdi:cellphone-arrow-down",
            tag = entity,
            until =  [{
                "entity_id" : entity,
                "new_state" : "off"}])

    """
    Callback triggered when a new upate is available on the HACS domain.
    Goals :
    . Notify
    """
    def callback_hacs_update_available(self, entity, attribute, old, new, kwargs):
        if new != "unknown":
            number_of_available_update = int(new)
            if number_of_available_update > 0:
                self.log("Detecting an available update... Notifying it...")
                self.fire_event("NOTIFIER",
                    action = "send_to_jl",
                    title = "🎉 Mise a jour HACS disponible",
                    message = "Une mise a jour HACS est disponible",
                    click_url = "/hacs/entry",
                    icon = "mdi:cellphone-arrow-down",
                    persistent = True,
                    tag = "hacs_update",
                    until =  [{
                        "entity_id" : entity,
                        "new_state" : 0}])

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
            color = "#ff6e07",
            persistent = True)
    """
    Callback triggered when the last available back-up is older than 24 hours.
    Goals :
    . Notify
    """
    def callback_samba_backup_daily_check(self, kwargs):
        self.log("Checking last Samba backup ...")
        last_backup_string = self.get_state("sensor.samba_backup", attribute = 'last_backup') + ":00"
        last_backup_date = self.parse_datetime(last_backup_string, aware = True)
        now = self.get_now()
        if (now - last_backup_date) > datetime.timedelta(hours = 24):
            self.log("Samba backup issue found... Notifying it")
            self.fire_event("NOTIFIER",
                action = "send_to_jl",
                title = "💾 Sauvegarde journalière",
                message = "La sauvegarde journalière sur le NAS n'a pas eu lieu depuis plus de 24 heures",
                click_url = "/lovelace-system/overview",
                icon =  "mdi:cloud-upload",
                color = "#ff6e07",
                persistent = True)

    """
    Callback triggered when the last available back-up is older than 24 hours.
    Goals :
    . Notify
    """
    def callback_battery_daily_check(self, kwargs):
        self.log("Checking battery levels  ...")
        
        battery_threshold = self.args["battery_threshold"]
        entities_to_notify = []

        for battery_sensor in self.args["battery_sensors_to_check"]:
            if int(self.get_state(battery_sensor)) < battery_threshold:
                friendly_name = self.get_state(battery_sensor, attribute = "friendly_name")
                entities_to_notify.append(friendly_name)
            
        if len(entities_to_notify) == 1:
            self.log("Low battery... Notifying it")
            self.fire_event("NOTIFIER",
                action = "send_to_jl",
                title = "Batterie 🪫",
                message= "Pensez a changer les piles de l'appareil suivant: " + entities_to_notify[0],
                icon =  "mdi:battery-20",
                color = "#ff6e07",
                persistent = True)
        
        elif len(entities_to_notify) > 1:
            self.log("Low battery... Notifying it")
            self.fire_event("NOTIFIER",
                action = "send_to_jl",
                title = "Batterie 🪫",
                message= "Pensez a changer les piles des appareils suivants: " + ", ".join(entities_to_notify),
                icon =  "mdi:battery-20",
                color = "#ff6e07",
                persistent = True)