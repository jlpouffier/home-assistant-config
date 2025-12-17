# Power Notification - Litière pleine / Power Notification - Litière pleine

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `button_action`: Reset Passages litière
- `button_title`: C'est fait!
- `default_message`: Pensez à nettoyer la litière !
- `default_title`: 🐈 Litière
- `discard_when`: Litière pleine (Cellier) to “off”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Home

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `button_action` : Action : reset sur Passages litière
- `button_title` : C'est fait!
- `default_message` : Pensez à nettoyer la litière !
- `default_title` : 🐈 Litière
- `discard_when` : Litière pleine (Cellier) à “off”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Maison
