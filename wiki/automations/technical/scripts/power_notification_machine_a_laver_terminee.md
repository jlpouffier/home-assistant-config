# Power Notification - Machine à laver terminée / Power Notification - Machine à laver terminée

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `button_action`: Set État machine à laver (Salle de bains) to “Inactive”
- `button_title`: Machine vidée!
- `default_message`: Cycle de lavage terminé !
- `default_title`: 🫧 Machine à laver
- `discard_when`: État machine à laver (Salle de bains) from “À vider”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Home

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `button_action` : Mettre État machine à laver (Salle de bains) sur “Inactive”
- `button_title` : Machine vidée!
- `default_message` : Cycle de lavage terminé !
- `default_title` : 🫧 Machine à laver
- `discard_when` : État machine à laver (Salle de bains) de “À vider”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Maison
