import hassapi as hass
import json
import random


class snips(hass.Hass): 
  def initialize(self):
    self.listen_state(self.callback_toggle_snips, "input_boolean.snips_switch")
    self.listen_event(self.callback_snips_event_received, "SNIPS_EVENT")
    self.listen_event(self.callback_snips_say, "SNIPS_SAY")
    self.log("Snips bot initialized")

  """
  Callback triggered when 
  """
  def callback_snips_event_received(self, event_name, data, kwargs):
    data_payload = json.loads(data['payload'])
    intent_summary = self.generate_intent_summary(data_payload)
    self.log("Snips intent received:")
    self.log_intent_summary(intent_summary)
    bom = {}

    if intent_summary['name'] == 'Jenova70:ActOnVacuum':
      bom = self.create_bom_act_on_vacuum(intent_summary)
      if bom:
        self.act_on_vacuum(bom)
    
    elif intent_summary['name'] == 'Jenova70:ActOnLight':
      bom = self.create_bom_act_on_light(intent_summary)
      if bom:
        self.act_on_light(bom)

    elif intent_summary['name'] == 'Jenova70:ArrivingHome':
      bom = self.create_bom_arriving_home(intent_summary)
      if bom:
        self.act_on_arriving_home(bom)    

    elif intent_summary['name'] == 'Jenova70:LeavingHome':
      bom = self.create_bom_leaving_home(intent_summary)
      if bom:
        self.act_on_leaving_home(bom)

    elif intent_summary['name'] == 'Jenova70:ActOnCover':
      bom = self.create_bom_act_on_cover(intent_summary)
      if bom:
        self.act_on_cover(bom)
    
    if not bom:
      #self.say_something("not_understood")
      self.call_service("mqtt/publish", topic = "snips/hotword/default/detected" , payload = "{\"siteId\": \"default\",\"modelId\": \"hey_snips\"}")



  """
  Callback triggered when 
  """
  def callback_snips_say(self, event_name, data, kwargs):
    if self.get_state("input_boolean.snips_switch") == 'on':
      self.log("Saying : " + data["payload"])
      self.say(data['payload'])

  """
  Callback triggered when 
  """
  def callback_toggle_snips(self, entity, attribute, old, new, kwargs):
    if old != new:
      if new == 'on':
        self.call_service("mqtt/publish", topic = "snips/hotword/toggleOn" , payload = "{\"siteId\":\"default\"}")
      if new == 'off':
        self.call_service("mqtt/publish", topic = "snips/hotword/toggleOff" , payload = "{\"siteId\":\"default\"}")

  """
  Helper method:
  Does : Act on light. See inside comments for more details !
  Returns :  Nothing
  """
  def act_on_light(self, bom):

    # Turn on lights ...
    if bom['action'] == 'on':
      # ... to 100% or to the requested intensity ...
      intensity = 100
      if 'intensity' in bom:
        intensity = bom['intensity']
      # ... for all rooms requested  ...
      if bom['rooms'] and 'all' not in bom['rooms']:
        for room in bom['rooms']:
          self.log("Turning on " + room + " at " + str(intensity) + "%")
          self.call_service('light/turn_on', entity_id = room, brightness_pct = intensity)

      # ... or by default for all rooms in the appartment 
      else:
        all_rooms = self.get_all_rooms("light")
        for room in all_rooms:
          self.log("Turning on " + room + " at " + str(intensity) + "%")
          self.call_service('light/turn_on', entity_id = room, brightness_pct = intensity)


    # turn off lights ...
    elif bom['action'] == 'off' and 'intensity' not in bom:
      # ... for all rooms requested  ...
      if bom['rooms'] and 'all' not in bom['rooms']:
        for room in bom['rooms']:
          self.log("Turning off " + room)
          self.call_service('light/turn_off', entity_id = room)
      # ... or by default for all rooms in the appartment 
      else:
        all_rooms = self.get_all_rooms("light")
        for room in all_rooms:
          self.log("Turning off " + room)
          self.call_service('light/turn_off', entity_id = room)

    # Set / Increase / Decrease lights ...
    elif (bom['action'] == 'set' or bom['action'] == 'decrease' or bom['action'] == 'increase') and 'intensity' in bom:
      intensity = bom['intensity']
      # ... for all rooms requested  ...
      if bom['rooms'] and 'all' not in bom['rooms']:
        for room in bom['rooms']:
          self.log("Turning on " + room + " at " + str(intensity) + "%")
          self.call_service('light/turn_on', entity_id = room, brightness_pct = intensity)
      # ... or by default for all rooms in the appartment 
      else:
        all_rooms = self.get_all_rooms("light")
        for room in all_rooms:
          self.log("Turning on " + room + " at " + str(intensity) + "%")
          self.call_service('light/turn_on', entity_id = room, brightness_pct = intensity)

    # Decrease light intensity by 2 ...
    elif bom['action'] == 'decrease' and 'intensity' not in bom:
      # ... for all rooms requested  ...
      if bom['rooms'] and 'all' not in bom['rooms']:
        for room in bom['rooms']:
          if self.get_state(room) == "on":
            current_intensity_254 = self.get_state(room, attribute = 'brightness')
            target_intensity_254 = int(current_intensity_254 / 2)
            target_intensity = int (target_intensity_254 * 100 / 254)
            self.log("Turning on " + room + " at " + str(target_intensity) + "%")
            self.call_service('light/turn_on', entity_id = room, brightness = target_intensity_254)
      # ... or by default for all rooms in the appartment 
      else:
        all_rooms = self.get_all_rooms("light")
        for room in all_rooms:
          if self.get_state(room) == "on":
            current_intensity_254 = self.get_state(room, attribute = 'brightness')
            target_intensity_254 = int(current_intensity_254 / 2)
            target_intensity = int (target_intensity_254 * 100 / 254)
            self.log("Turning on " + room + " at " + str(target_intensity) + "%")
            self.call_service('light/turn_on', entity_id = room, brightness = target_intensity_254)

    # Increase light intensity by 2 ...
    elif bom['action'] == 'increase' and 'intensity' not in bom:
      # ... for all rooms requested  ...
      if bom['rooms'] and 'all' not in bom['rooms']:
        for room in bom['rooms']:
          if self.get_state(room) == "on":
            current_intensity_254 = self.get_state(room, attribute = 'brightness')
            target_intensity_254 = min(int(current_intensity_254 * 2) , 254)
            target_intensity = int (target_intensity_254 * 100 / 254)
            self.log("Turning on " + room + " at " + str(target_intensity) + "%")
            self.call_service('light/turn_on', entity_id = room, brightness = target_intensity_254)
      # ... or by default for all rooms in the appartment 
      else:
        all_rooms = self.get_all_rooms("light")
        for room in all_rooms:
          if self.get_state(room) == "on":
            current_intensity_254 = self.get_state(room, attribute = 'brightness')
            target_intensity_254 = min(int(current_intensity_254 * 2) , 254)
            target_intensity = int (target_intensity_254 * 100 / 254)
            self.log("Turning on " + room + " at " + str(target_intensity) + "%")
            self.call_service('light/turn_on', entity_id = room, brightness = target_intensity_254)

  """
  Helper method:
  Does : Turn on the Vaccum, or request the RTH. Verbal feedback via snips
  Returns :  Nothing
  """
  def act_on_vacuum(self, bom):
    if bom['action'] == 'on':
      self.say('Lancement de Spirou')
      self.log("Starting sprioo")
      self.call_service("neato/custom_cleaning" , entity_id = "vacuum.spiroo" , category = 4 , mode  = 1 , navigation = 1)
    elif bom['action'] == 'off':
      self.say('Retour de Spirou à sa base')
      self.log("Stoping sprioo")
      self.call_service("vacuum/return_to_base" , entity_id = "vacuum.spiroo")

  """
  Helper method:
  Does : Turn off all lights. Turn off the TV. Verbal feedback via snips
  Returns :  Nothing
  """
  def act_on_leaving_home(self, bom):
    if bom["action"]:
      self.say_something("farewell")
      self.log("Turning off TV")
      self.call_service("media_player/turn_off" , entity_id = "media_player.philips_android_tv")
      sequence = [
        {"sleep": 1},
        {"light/turn_off": {
          "entity_id": "light.chambre_principale",
          "transition": 5 }},
        {"light/turn_off": {
          "entity_id": "light.chambre_secondaire",
          "transition": 5 }},
        {"sleep": 4},
        {"light/turn_off": {
          "entity_id": "light.cuisine",
          "transition": 5 }},
        {"light/turn_off": {
          "entity_id": "light.salon",
          "transition": 5 }},
        {"sleep": 4},
        {"light/turn_off": {
          "entity_id": "light.entree",
          "transition": 5 }}
      ]
      self.log("Turning off lights")
      self.run_sequence(sequence)


  """
  Helper method:
  Does : Turn on the lights of the entry, living room and kitchen. Verbal feedback via snips
  Returns :  Nothing
  """
  def act_on_arriving_home(self, bom):
    if bom["action"]:
      self.say_something("greeting")
      sequence = [
        {"sleep": 1},
        {"light/turn_on": {
          "entity_id": "light.entree",
          "transition": 3,
          "brightness_pct": 100 }},
        {"sleep": 2},
        {"light/turn_on": {
          "entity_id": "light.salon",
          "transition": 3,
          "brightness_pct": 100 }},
        {"sleep": 2},
        {"light/turn_on": {
          "entity_id": "light.cuisine",
          "transition": 3,
          "brightness_pct": 100 }}
      ]
      self.log("Turning on lights")
      self.run_sequence(sequence)


  """
  Helper method:
  Does : Act on Cover. See inside comments for more details !
  Returns :  Nothing
  """
  def act_on_cover(self, bom):
    # Set specific position to the covers ...
    if (bom["action"] == "open" or bom["action"] == "close" or bom["action"] == "set") and 'intensity' in bom:
      
      # Open / Set case : Target position is input 
      if bom["action"] == "open" or bom["action"] == "set" :
        target_position = bom['intensity']

      # Close case : Target position is 100 - input 
      elif bom["action"] == "close":
        target_position = 00 - bom['intensity']

    # Set the cover target position ...

      # ... for all rooms requested  ...
      if bom['rooms'] and 'all' not in bom['rooms']:
        for room in bom["rooms"]:
          if room:
            self.log("Setting " + room + " at " + str(target_position) + "%")
            self.call_service("cover/set_cover_position", entity_id = room, position = target_position)
      # ... or by default for all rooms in the appartment 
      else:
        all_rooms = self.get_all_rooms("cover")
        for room in all_rooms:
          self.log("Setting " + room + " at " + str(target_position) + "%")
          self.call_service("cover/set_cover_position", entity_id = room, position = target_position)


    # Open covers (all the way)
    elif bom["action"] == "open" and 'intensity' not in bom:
      # ... for all rooms requested  ...
      if bom['rooms'] and 'all' not in bom['rooms']:
        for room in bom["rooms"]:
          if room:
            self.log("Opening " + room)
            self.call_service("cover/open_cover", entity_id = room)
      # ... or by default for all rooms in the appartment 
      else:
        all_rooms = self.get_all_rooms("cover")
        for room in all_rooms:
          self.log("Opening " + room)
          self.call_service("cover/open_cover", entity_id = room)

    # Close covers (all the way)      
    elif bom["action"] == "close" and 'intensity' not in bom:
      # ... for all rooms requested  ...
      if bom['rooms'] and 'all' not in bom['rooms']:
        for room in bom["rooms"]:
          if room:
            self.log("Closing " + room)
            self.call_service("cover/close_cover", entity_id = room)
      # ... or by default for all rooms in the appartment 
      else:
        all_rooms = self.get_all_rooms("cover")
        for room in all_rooms:
          self.log("Closing " + room)
          self.call_service("cover/close_cover", entity_id = room)


    # Stop the covers ...
    elif bom["action"] == "stop" and 'intensity' not in bom:
      # ... for all rooms requested  ...
      if bom['rooms'] and 'all' not in bom['rooms']:
        for room in bom["rooms"]:
          if room:
            self.log("Stopping " + room)
            self.call_service("cover/stop_cover", entity_id = room)
      # ... or by default for all rooms in the appartment 
      else:
        all_rooms = self.get_all_rooms("cover")
        for room in all_rooms:
          self.log("Stopping " + room)
          self.call_service("cover/stop_cover", entity_id = room)


  """
  Helper method:
  Does : publish a topic that will trigger a Snips text to speech action (Snips will talk) 
  Returns :  Nothing
  Warning : Doc of Snips (https://docs.snips.ai/reference/hermes#text-to-speech-tts) is informing me that this is a very low level AP, not suited for production. But I do not want (for now) to handle dialog management.
  """    
  def say(self, text): 
    self.call_service("mqtt/publish", topic = "snips/tts/say" , payload = "{\"siteId\": \"default\",\"text\": \"" + text + "\", \"lang\": \"fr\",\"sessionId\": null}")

  """
  Helper method:
  Does : Say random senteces based on category
  Returns :  Nothing
  """
  def say_something(self, category): 
    choice = []
    if category == 'greeting':
      choices = [ 
        "Bonjour", 
        "Bienvenue", 
        "Bienvenue à la maison", 
        "Bienvenue chez vous",
        "Bonjour, bienvenue à la maison", 
        "Bonjour, bienvenue chez vous",
        "Ravie de vous revoir"
      ]

    elif category == 'farewell':
      choices = [
        "À très bientôt",
        "À très vite",
        "À bientôt",
        "À la prochaine",
        "Revenez vite",
        "Au revoir",
        "Amusez-vous bien !"
      ]

    elif category == 'not_understood':
      choices = [
        "Désolé je ne suis pas sur d'avoir compris",
        "Pardon ?",
        "Pouvez-vous répéter ?",
        "Je ne suis pas sur d'avoir compris",
        "Pardon, pouvez-vous répéter ?"
      ]

    self.say(random.choice(choices))


  """
  Helper method:
  Does : Streamline the data receveid in the payload of the event. Keep only what is needed for the rest of the process.
  Returns :  The intent summary
  Here is an example :
  TODO
  """
  def generate_intent_summary(self, data_payload):
    intent_summary = {}
    if 'intent' in data_payload and 'intentName' in data_payload['intent'] and 'confidenceScore' in data_payload['intent']:
      intent_summary['name'] = data_payload['intent']['intentName']
      intent_summary['confidence'] = data_payload['intent']['confidenceScore']
    if 'slots' in  data_payload:
      slots = []
      for slot in data_payload['slots']:
        slot_intent_summary = {}
        if 'slotName' in slot and 'entity' in slot and 'confidenceScore' in slot and 'value' in slot and 'value' in slot['value']:
          slot_intent_summary['name'] = slot['slotName']
          slot_intent_summary['type'] = slot['entity']
          slot_intent_summary['confidence'] = slot['confidenceScore']
          slot_intent_summary['value'] = slot['value']['value']
        slots.append(slot_intent_summary)
      intent_summary['slots'] = slots
    return intent_summary

  
  """
  Helper method:
  Does : log intent 
  Returns :  nothing
  """
  def log_intent_summary(self, intent_summary):
    if "name" in intent_summary and "confidence" in intent_summary:
      self.log(intent_summary["name"] + " [" + str(intent_summary["confidence"]) + "]")
    if "slots" in intent_summary:
      for slot in intent_summary["slots"]:
        if "type" in slot and "value" in slot and "confidence" in slot:
          self.log("  > " + str(slot))


  """
  Helper method:
  Does : Check if the intent in input is coherent for an action on a vaccum
  Returns :  True or False depending if the intent is coherent
  """
  def is_intent_coherent_for_act_on_vacuum(self, intent_summary):
    # Overall confidence needs to be at least 70 %
    if intent_summary["confidence"] < 0.7:
      return False
    # Confidence of each slots need to be at least 50 %
    for slot in intent_summary['slots']:
      if slot["confidence"] < 0.5:
        return False 
        
    # You can have only one slot and the type needs to be "action".
    if len(intent_summary['slots']) == 1 and intent_summary['slots'][0]['name'] == 'action':
        return True
    else:
        return False
  
  """
  Helper method:
  Does : Check if the intent in input is coherent for an action on light
  Returns :  True or False depending if the intent is coherent
  """  
  def is_intent_coherent_for_act_on_light(self, intent_summary):
    # Overall confidence needs to be at least 70 %
    if intent_summary["confidence"] < 0.7:
      return False
    
    # Confidence of each slots need to be at least 20 % (Maybe I could increase a bit this value now that I fixed Snips...)
    for slot in intent_summary['slots']:
      if slot["confidence"] < 0.2:
        return False
    room_slots=[]
    intensity_slots=[]
    action_slots=[]
    for slot in intent_summary['slots']:
      if slot['name'] == 'action':
        action_slots.append(slot)
      elif slot['name'] == 'room':
        room_slots.append(slot)
      elif slot['name'] == 'intensity':
        intensity_slots.append(slot)
        
    # You can have only one action
    if len(action_slots) != 1: 
      return False
    
    # You can either have 0 or 1 intensity value
    if len(intensity_slots) > 1:
      return False
      
    return True


  """
  Helper method:
  Does : Check if the intent in input is coherent for an action on cover
  Returns :  True or False depending if the intent is coherent
  """  
  def is_intent_coherent_for_act_on_cover(self, intent_summary):
    # Overall confidence needs to be at least 70 %
    if intent_summary["confidence"] < 0.7:
      return False
    
    # Confidence of each slots need to be at least 50 %
    for slot in intent_summary['slots']:
      if slot["confidence"] < 0.5:
        return False
    room_slots=[]
    intensity_slots=[]
    action_slots=[]
    for slot in intent_summary['slots']:
      if slot['name'] == 'action':
        action_slots.append(slot)
      elif slot['name'] == 'room':
        room_slots.append(slot)
      elif slot['name'] == 'intensity':
        intensity_slots.append(slot)
        
    # You can have only one action
    if len(action_slots) != 1: 
      return False
    
    # You can either have 0 or 1 intensity value
    if len(intensity_slots) > 1:
      return False
      
    return True


  """
  Helper method:
  Does : Check if the intent in input is coherent, create a bom
  Returns :  A simple bom that will repreent the action to be perfomred on the vaccum.
  Here is an example :
  {
    "action": "on"
  }
  """
  def create_bom_act_on_vacuum(self, intent_summary):
    bom = {}
    # Check if the intent is coherent
    if self.is_intent_coherent_for_act_on_vacuum(intent_summary):
      # Create the bom ...
      slot = intent_summary['slots'][0]
      bom["action"] = self.translate_slot_value(slot['type'], slot['value'])
    return bom

  """
  Helper method:
  Does : Check if the intent in input is coherent, create a bom
  Returns :  A simple bom that will repreent the action to be perfomred on a light.
  Here is an example :
  {
    "action": "on",
    "rooms": ["light.chambre_principale", "light.cuisine", "light.entree"],
    "intensity": "60"
  }
  """
  def create_bom_act_on_light(self, intent_summary):
    bom = {}
    # Check if the intent is coherent 
    if self.is_intent_coherent_for_act_on_light(intent_summary):
      # Create the bom ...
      room_slots=[]
      intensity_slots=[]
      action_slots=[]
      for slot in intent_summary['slots']:
        if slot['name'] == 'action':
          action_slots.append(slot)
        elif slot['name'] == 'room':
          room_slots.append(slot)
        elif slot['name'] == 'intensity':
          intensity_slots.append(slot)
      bom["action"] = self.translate_slot_value(action_slots[0]['type'], action_slots[0]['value'])
      bom['rooms'] = []
      for slot in room_slots:
          bom['rooms'].append(self.translate_slot_value(slot['type'], slot['value'], "light"))
      if len(intensity_slots) == 1:
          bom['intensity'] = intensity_slots[0]['value']
    return bom

  def create_bom_arriving_home(self, intent_summary):
    if intent_summary["confidence"] < 0.6:
      return {}
    else:
      return {'action':True}

  def create_bom_leaving_home(self, intent_summary):
    if intent_summary["confidence"] < 0.6:
      return {}
    else:
      return {'action':True}

  """
  Helper method:
  Does : Check if the intent in input is coherent, create a bom
  Returns :  A simple bom that will repreent the action to be perfomred on a cover.
  Here is an example :
  {
    "action": "open",
    "rooms": ["cover.main_bedroom_roller_shutter"],
    "intensity": "70"
  }
  """
  def create_bom_act_on_cover(self, intent_summary):
    bom = {}
    if self.is_intent_coherent_for_act_on_cover(intent_summary):
      room_slots=[]
      intensity_slots=[]
      action_slots=[]
      for slot in intent_summary['slots']:
        if slot['name'] == 'action':
          action_slots.append(slot)
        elif slot['name'] == 'room':
          room_slots.append(slot)
        elif slot['name'] == 'intensity':
          intensity_slots.append(slot)
      bom["action"] = self.translate_slot_value(action_slots[0]['type'], action_slots[0]['value'])
      bom['rooms'] = []
      for slot in room_slots:
          bom['rooms'].append(self.translate_slot_value(slot['type'], slot['value'], "cover"))
      if len(intensity_slots) == 1:
          bom['intensity'] = intensity_slots[0]['value']
    return bom

  """
  Helper method:
  Does : Nothing
  Returns :  An array of all the entity ID of the room in the appartment (It's static unformtunately - I could do better)
  """
  def get_all_rooms(self, context = "light"):
    if context == "light":
      return ["light.entree" , "light.salon" , "light.cuisine" ,  "light.chambre_principale" , "light.chambre_secondaire"]
    if context == "cover":
      return ["cover.main_bedroom_roller_shutter"]
    else:
      return []

  """
  Helper method:
  Does : Nothing
  Returns :  the translated value of a slot
  . For a room : Directly the home assistant entity id that will be used in the service call (or all)
  . For actions (light or vacuum or cover) a simple keyword that will be used to drive what will be done
  Returns directly the input slot value if not translated (best effort)
  """
  def translate_slot_value(self, slot_type, slot_value, context = 'light'):
    translations = {}
    
    # Rooms of the appartment
    if slot_type == "house/room" and context  == "light":
      translations = {
        "chambre principale":"light.chambre_principale",
        "chambre secondaire":"light.chambre_secondaire",
        "salon":"light.salon",
        "cuisine":"light.cuisine",
        "entree":"light.entree",
        "maison":"all"
      }
      
    elif slot_type == "house/room" and context  == "cover":
      translations = {
        "chambre principale":"cover.main_bedroom_roller_shutter",
        "chambre secondaire":"",
        "salon":"",
        "cuisine":"",
        "entree":"",
        "maison":"all"
      }
    # Possible actions on a light 
    elif slot_type == "light/action":
      translations = {
        "augmente":"increase",
        "diminue":"decrease",
        "regle":"set",
        "eteins":"off",
        "allume":"on"
      }
      
    # Possible actions  on the vaccum
    elif slot_type == "vacuum/action":
      translations = {
        "arrête":"off",
        "démarre":"on"
      }
    
    elif slot_type == "cover/action":
      translations = {
        "stoppe":"stop",
        "regle":"set",
        "ouvre":"open",
        "ferme":"close"
      }

    # If the transaltion worked : Return the translated value, else : Return the input value
    if slot_value in translations:
      return translations[slot_value]
    else:
      return slot_value
