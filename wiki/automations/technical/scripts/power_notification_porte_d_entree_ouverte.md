# Power Notification - Porte d'entrée ouverte lors du départ / Power Notification - Porte d'entrée ouverte lors du départ

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `default_importance`: True
- `default_message`: La porte d'entrée est toujours ouverte alors que vous allez partir!
- `default_title`: 🚪Porte d'entrée
- `discard_when`: Porte d'entrée (Entrée) to “off”; Modes de presence de la maison to “Occupée”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Proche de la maison

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `default_importance` : True
- `default_message` : La porte d'entrée est toujours ouverte alors que vous allez partir!
- `default_title` : 🚪Porte d'entrée
- `discard_when` : Porte d'entrée (Entrée) à “off”; Modes de presence de la maison à “Occupée”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Proche de la maison
