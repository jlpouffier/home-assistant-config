# jlo/power_notification_creator.yaml / jlo/power_notification_creator.yaml

## English
- Source file: `blueprints/script/jlo/power_notification_creator.yaml`

### Power Notification Creator

Send powerfull notifications that discard themselves to the people of the home depending on where they are. This blueprint must be used everytime you want to configure a new notification. It will create a script that you can call everytime you want to send it.

### Inputs
- `advanced_section`
- `button`
- `content`
- `discard`
- `target`

### What the blueprint does (high level)
- Repeat
- If A computed rule is true
- Generate data
- Item]['service']}}
- Else
- Item]['service']}}
- If A computed rule is true
- Wait for trigger: An event happens
- Or trigger: A trigger fires
- If A computed rule is true
- Repeat
- Item]['service']}}

```mermaid
flowchart TD
  S["Start"]
  N1["Repeat"]
  N2["If A computed rule is true"]
  N3["Generate data"]
  N4["Item]['service']}}"]
  N5["Else"]
  N6["Item]['service']}}"]
  N7["If A computed rule is true"]
  N8["Wait for trigger: An event happens"]
  N9["Or trigger: A trigger fires"]
  N10["If A computed rule is true"]
  N11["Repeat"]
  N12["Item]['service']}}"]
  E["End"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> N7
  N7 --> N8
  N8 --> N9
  N9 --> N10
  N10 --> N11
  N11 --> N12
  N12 --> E
```

## Français
- Fichier source : `blueprints/script/jlo/power_notification_creator.yaml`

### Power Notification Creator

Send powerfull notifications that discard themselves to the people of the home depending on where they are. This blueprint must be used everytime you want to configure a new notification. It will create a script that you can call everytime you want to send it.

### Entrées
- `advanced_section`
- `button`
- `content`
- `discard`
- `target`

### Ce que fait le blueprint (niveau simple)
- Répéter
- Si Une règle calculée est vraie
- Action : generate data
- Action : item]['service']}}
- Sinon
- Action : item]['service']}}
- Si Une règle calculée est vraie
- Attendre le déclencheur : Un événement se produit
- Ou : Un déclencheur se produit
- Si Une règle calculée est vraie
- Répéter
- Action : item]['service']}}

```mermaid
flowchart TD
  S["Début"]
  N1["Répéter"]
  N2["Si Une règle calculée est vraie"]
  N3["Action : generate data"]
  N4["Action : item]['service']}}"]
  N5["Sinon"]
  N6["Action : item]['service']}}"]
  N7["Si Une règle calculée est vraie"]
  N8["Attendre le déclencheur : Un événement se produit"]
  N9["Ou : Un déclencheur se produit"]
  N10["Si Une règle calculée est vraie"]
  N11["Répéter"]
  N12["Action : item]['service']}}"]
  E["Fin"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> N7
  N7 --> N8
  N8 --> N9
  N9 --> N10
  N10 --> N11
  N11 --> N12
  N12 --> E
```
