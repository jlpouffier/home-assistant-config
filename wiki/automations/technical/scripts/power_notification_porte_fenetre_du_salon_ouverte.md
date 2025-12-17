# Power Notification - Porte fenêtre du salon ouverte / Power Notification - Porte fenêtre du salon ouverte

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `default_importance`: False
- `default_message`: La porte fenêtre du salon est toujours ouverte alors que vous allez partir!
- `default_title`: 🚪Porte fenêtre du salon
- `discard_when`: Porte fenêtre (Salon) to “off”; Modes de presence de la maison to “Occupée”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Proche de la maison

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `default_importance` : False
- `default_message` : La porte fenêtre du salon est toujours ouverte alors que vous allez partir!
- `default_title` : 🚪Porte fenêtre du salon
- `discard_when` : Porte fenêtre (Salon) à “off”; Modes de presence de la maison à “Occupée”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Proche de la maison
