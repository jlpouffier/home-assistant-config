# Power Notification - Poubelle Verte à sortir / Power Notification - Poubelle Verte à sortir

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `button`: True
- `button_action`: Turn off Poubelle verte à sortir (Rue)
- `button_title`: C'est fait!
- `default_message`: N'oubliez pas de sortir la poubelle verte
- `default_title`: ♻️ Poubelle Verte
- `discard_when`: Poubelle verte à sortir (Rue) to “off”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Home

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `button` : True
- `button_action` : Désactiver Poubelle verte à sortir (Rue)
- `button_title` : C'est fait!
- `default_message` : N'oubliez pas de sortir la poubelle verte
- `default_title` : ♻️ Poubelle Verte
- `discard_when` : Poubelle verte à sortir (Rue) à “off”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Maison
