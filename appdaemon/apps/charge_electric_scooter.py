import hassapi as hass

"""
clean_house is an app responsible of reminding us to charge our electric scoooter

Functionalities :
    Guess when the electric scooter is charged or not based on Valentin's location

Notifications :
    Charging needed.
"""
class charge_electric_scooter(hass.Hass):
    def initialize(self):
        self.listening_to_valentine_coming_back_home = False
        self.listen_state(self.callback_valentine_at_work, "person.valentine", new = "BackMarket (Bordeaux)", immediate = True)
        self.listen_state(self.callback_electric_scooter_charging, "binary_sensor.is_electric_scooter_charging", new = "on" , immediate = True)
        self.run_daily(self.callback_electric_scooter_daily_check, "20:00:00")

    """
    Callback triggered when valentine reaches work
    Goals :
        Concider electric scooter discharged
    """ 
    def callback_valentine_at_work(self, entity, attribute, old, new, kwargs):
        self.log("Valentine arrived at work: Considerig that her electric scooter needs charging.")
        self.call_service("input_boolean/turn_on", entity_id = "input_boolean.electric_scooter_needs_charging")

    """
    Callback triggered when the eletrical outlet charging the scooter os powered
    Goals :
        Concider electric scooter charged
    """ 
    def callback_electric_scooter_charging(self, entity, attribute, old, new, kwargs):
        self.log("Electric Scooter charging: Considering that it does not need charing anymore.")
        self.call_service("input_boolean/turn_off", entity_id = "input_boolean.electric_scooter_needs_charging")

    """
    Callback triggered everyday at 8pm 
    Goals :
        If valentine is at work, check if we need to send the notification
        Else: Wait until valentine reaches home
    """ 
    def callback_electric_scooter_daily_check(self, kwargs):
        if self.entities.person.valentine.state == "home":
            self.check_electric_scooter_and_send_notification()
        else:
            if not self.listening_to_valentine_coming_back_home:
                self.listening_to_valentine_coming_back_home = True
                self.listen_state(self.callback_valentine_at_home, "person.valentine", new = "home", duration = "900" , oneshot = True)
    
    """
    Callback triggered when valentine reaches work Valentine reaches home
    Goals :
        check if we need to send the notification
    """ 
    def callback_valentine_at_home(self, entity, attribute, old, new, kwargs):
        self.listening_to_valentine_coming_back_home = False
        self.check_electric_scooter_and_send_notification()

    """
    Helper method:
    Does : 
    . If tomorrow is a workday, and the electric scooter is discharged: Send notification
    Returns : Noting
    """
    def check_electric_scooter_and_send_notification(self):
        if self.entities.input_boolean.electric_scooter_needs_charging.state == "on" and self.entities.binary_sensor.workday_tomorrow.state == "on":
            self.log("It's time to charge the electric scooter. notifying it")
            self.fire_event("NOTIFIER",
                action = "send_to_valentine",
                title = "🛴 Trottinette",
                message = "Pense à faire charger ta trottinette pour demain !",
                click_url = "/lovelace/terrasse",
                icon =  "mdi:scooter-electric",
                color = "deep-orange",
                tag = "electric_scooter",
                until =  [{
                    "entity_id" : "input_boolean.electric_scooter_needs_charging",
                    "new_state" : "off"}])



