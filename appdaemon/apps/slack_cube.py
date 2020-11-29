import hassapi as hass


class slack_cube(hass.Hass): 
  def initialize(self):
    self.listen_state(self.callback , "sensor.cube_face" )

  def callback(self, entity, attribute, old, new, kwargs):
    if new == "FACE_1":
      self.call_service("rest_command/slack_change_status", status = "Away", emoji = ":away:")
    if new == "FACE_2":
      self.call_service("rest_command/slack_change_status", status = "Do not disturb !", emoji = ":shushing_face:")
    if new == "FACE_3":
      self.call_service("rest_command/slack_change_status", status = "Here", emoji = ":here:")
    if new == "FACE_4":
      self.call_service("rest_command/slack_change_status", status = "Coffee break", emoji = ":coffee:")
    if new == "FACE_5":
      self.call_service("rest_command/slack_change_status", status = "Meeting", emoji = ":calendar:")
    if new == "FACE_6":
      self.call_service("rest_command/slack_change_status", status = "Eating", emoji = ":chef-brb:")
