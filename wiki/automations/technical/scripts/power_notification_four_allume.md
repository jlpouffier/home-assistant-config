# Power Notification - Four allumé / Power Notification - Four allumé

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `default_importance`: True
- `default_message`: Le four est en marche alors que vous allez partir!
- `default_title`: 🥘 Four allumé
- `discard_when`: Four En cours d'utilisation (Cuisine) to “off”; Modes de presence de la maison to “Occupée”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Proche de la maison

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `default_importance` : True
- `default_message` : Le four est en marche alors que vous allez partir!
- `default_title` : 🥘 Four allumé
- `discard_when` : Four En cours d'utilisation (Cuisine) à “off”; Modes de presence de la maison à “Occupée”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Proche de la maison
