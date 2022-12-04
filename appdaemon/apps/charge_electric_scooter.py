import hassapi as hass

"""
charge_electric_scooter is an app responsible of 
"""
class charge_electric_scooter(hass.Hass):
    def initialize(self):
        self.listening_to_valentine_coming_back_home = False
        # Minimum Cleaning Duration. 
        self.listen_state(self.callback_valentine_at_work, "person.valentine", new = "BackMarket (Bordeaux)", immediate = True)
        self.listen_state(self.callback_electric_scooter_charging, "binary_sensor.is_electric_scooter_charging", new = "on" , immediate = True)
        self.run_daily(self.callback_electric_scooter_daily_check, "20:00:00")
        self.log("Initialized")

    def callback_valentine_at_work(self, entity, attribute, old, new, kwargs):
        self.log("Valentine arrived at work: Considerig that her electric scooter needs charging.")
        self.call_service("input_boolean/turn_on", entity_id = "input_boolean.electric_scooter_needs_charging")
    
    def callback_electric_scooter_charging(self, entity, attribute, old, new, kwargs):
        self.log("Electric Scooter charging: Considering that it does not need charing anymore.")
        self.call_service("input_boolean/turn_off", entity_id = "input_boolean.electric_scooter_needs_charging")

    def callback_electric_scooter_daily_check(self, kwargs):
        if self.get_state("person.valentine") == "home":
            self.check_electric_scooter_and_send_notification()
        else:
            if not self.listening_to_valentine_coming_back_home:
                self.listening_to_valentine_coming_back_home = True
                self.listen_state(self.callback_valentine_at_home, "person.valentine", new = "home", duratin = "900" , oneshot = True)
    
    def callback_valentine_at_home(self, entity, attribute, old, new, kwargs):
        self.listening_to_valentine_coming_back_home = False
        self.check_electric_scooter_and_send_notification()

    def check_electric_scooter_and_send_notification(self):
        if self.get_state("input_boolean.electric_scooter_needs_charging") == "on" and self.get_state("binary_sensor.workday_tomorrow") == "on":
            self.log("It's time to charge the electric scooter. notifying it")
            self.fire_event("NOTIFIER",
                action = "send_to_valentine",
                title = "🛴 Trottinette",
                message = "Pense à faire charger ta trottinette pour demain !",
                click_url = "/lovelace-system/overview",
                icon =  "mdi:scooter-electric",
                color = "#ff6e07",
                tag = "electric_scooter",
                until =  [{
                    "entity_id" : "input_boolean.electric_scooter_needs_charging",
                    "new_state" : "off"}])



