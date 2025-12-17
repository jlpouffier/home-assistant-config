# Power Notification - Lancement lave vaisselle prévu / Power Notification - Lancement lave vaisselle prévu

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `default_message`: Le lave vaisselle démarrera automatiquement cette nuit
- `default_title`: 🧽 Lave vaisselle
- `discard_when`: État lave vaisselle from “Planifié”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Home

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `default_message` : Le lave vaisselle démarrera automatiquement cette nuit
- `default_title` : 🧽 Lave vaisselle
- `discard_when` : État lave vaisselle de “Planifié”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Maison
