# Power Notification - Lave vaisselle terminé / Power Notification - Lave vaisselle terminé

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `button_action`: Set État lave vaisselle to “Inactif”
- `button_title`: Lave vaisselle vidé!
- `default_message`: Cycle de lavage terminé !
- `default_title`: 🧽 Lave vaisselle
- `discard_when`: État lave vaisselle from “À vider”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Home

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `button_action` : Mettre État lave vaisselle sur “Inactif”
- `button_title` : Lave vaisselle vidé!
- `default_message` : Cycle de lavage terminé !
- `default_title` : 🧽 Lave vaisselle
- `discard_when` : État lave vaisselle de “À vider”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Maison
