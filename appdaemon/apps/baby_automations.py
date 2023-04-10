import hassapi as hass

"""
baby_automations is an app responsible of helping us to know when to give the next baby bottle fto our daugther
"""
class baby_automations(hass.Hass):
    def initialize(self):
        self.listen_state(self.callback_bibi_incoming, "sensor.bouton_bibi_action", new = "press")
        self.scheduler_handles = []
        self.log("Initialized")

    def callback_bibi_incoming(self, entity, attribute, old, new, kwargs):
        self.log("Bibi incoming ... Starting countdown")

        while len(self.scheduler_handles) >=1:
            handle = self.scheduler_handles.pop()
            self.cancel_timer(handle)

        self.scheduler_handles.append(self.run_in(self.callback_next_bibi_possible, self.args["minimum_delay_between_bibi_in_hours"] * 60 * 60))
        self.scheduler_handles.append(self.run_in(self.callback_next_bibi_optimal, self.args["optimal_delay_between_bibi_in_hours"] * 60 * 60))
        self.scheduler_handles.append(self.run_in(self.callback_next_bibi_needed, self.args["maximum_delay_between_bibi_in_hours"] * 60 * 60))
    
    def callback_next_bibi_possible(self, kwargs):
        self.log("callback_next_bibi_possible")
        self.fire_event("NOTIFIER",
            action = "send_to_all",
            title = "🧸 " + self.args["kid_name"], 
            message = self.args["kid_name"] + " a pris son bibi il y a 2 heures, prochain Bibi possible",
            click_url="/lovelace/apercu",
            icon =  "mdi:baby-bottle",
            color = "#07ffc1",
            tag = "baby_bottle")
    
    def callback_next_bibi_optimal(self, kwargs):
        self.log("callback_next_bibi_optimal")
        self.fire_event("NOTIFIER",
            action = "send_to_all",
            title = "🧸 " + self.args["kid_name"],  
            message = self.args["kid_name"] + " a pris son bibi il y a 4 heures, prochain Bibi recommandé",
            click_url="/lovelace/apercu",
            icon =  "mdi:baby-bottle",
            color = "#07ffc1",
            tag = "baby_bottle")
    
    def callback_next_bibi_needed(self, kwargs):
        self.log("callback_next_bibi_needed")
        self.fire_event("NOTIFIER",
            action = "send_to_all",
            title = "🧸 " + self.args["kid_name"],  
            message = self.args["kid_name"] + " a pris son bibi il y a 6 heures, prochain Bibi nécessaire",
            click_url="/lovelace/apercu",
            icon =  "mdi:baby-bottle",
            color = "#07ffc1",
            tag = "baby_bottle")