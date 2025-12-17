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

### Flow (trace-style)
- Entry: when the blueprint is executed by a script/automation
- REPEAT
  - IF
    - Check: A custom rule is true (based on: Notifications Droles)
    - THEN
      - Generate structured data
      - Item]['service']}}
    - ELSE
      - Item]['service']}}
- IF
  - Check: A custom rule is true
  - THEN
    - Wait for one of: An event happens; A trigger fires
    - IF
      - Check: A custom rule is true
      - THEN
        - Step
    - REPEAT
      - Item]['service']}}

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

### Déroulé (style ‘trace’)
- Entrée : quand le blueprint est exécuté par un script/une automatisation
- RÉPÉTER
  - SI
    - Vérifier : Une règle personnalisée est vraie (basée sur : Notifications Droles)
    - ALORS
      - Générer des données structurées
      - Action : item]['service']}}
    - SINON
      - Action : item]['service']}}
- SI
  - Vérifier : Une règle personnalisée est vraie
  - ALORS
    - Attendre l’un de : Un événement se produit; Un déclencheur se produit
    - SI
      - Vérifier : Une règle personnalisée est vraie
      - ALORS
        - Étape
    - RÉPÉTER
      - Action : item]['service']}}
