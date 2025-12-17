# Power Notification - Lancement machine à laver prévu / Power Notification - Lancement machine à laver prévu

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `default_message`: La machine à laver démarrera automatiquement cette nuit
- `default_title`: 🫧 Machine à laver
- `discard_when`: État machine à laver (Salle de bains) from “Plannifiée”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Home

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `default_message` : La machine à laver démarrera automatiquement cette nuit
- `default_title` : 🫧 Machine à laver
- `discard_when` : État machine à laver (Salle de bains) de “Plannifiée”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Maison
