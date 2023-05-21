import hassapi as hass

"""
walkie_talkie is an app responsible of the handle my ESP based Walkie Talkie Voice Assistant

Functionalities :
    Cycle throught the available assistant by pressing a button on the talkie walkie
    Reset the assistant if the walkie talkie is not used for a period of time

Notifications :
    None

"""
class walkie_talkie(hass.Hass):
    def initialize(self):
        self.assistants_available = self.args["assistants_available"]
        self.listen_state(self.callback_change_assistant_button_pressed, "binary_sensor.talkie_change_assistant_button", new = "on")
        self.listen_state(self.callback_walkie_talkie_not_used_anymore, "binary_sensor.talkie_assistant_en_cours", new = "off", duration = 60)

    def callback_change_assistant_button_pressed(self, entity, attribute, old, new, kwargs):
        current_assistant = self.entities.select.talkie_pipeline_d_assistant.state

        if current_assistant in self.assistants_available:
            next_assistant = self.assistants_available[ (self.assistants_available.index(current_assistant) + 1) % len(self.assistants_available)]
        else:
            next_assistant = self.assistants_available[0]

        self.call_service("select/select_option", entity_id = "select.talkie_pipeline_d_assistant", option = next_assistant)

        tts_message = "Vous êtes en communication avec " + next_assistant
        self.call_service("tts/cloud_say", entity_id = "media_player.talkie_media_player", message = tts_message, language = "fr-FR")


    def callback_walkie_talkie_not_used_anymore(self, entity, attribute, old, new, kwargs):
        self.call_service("select/select_option", entity_id = "select.talkie_pipeline_d_assistant", option = self.assistants_available[0])