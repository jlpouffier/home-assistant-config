# Power Notification - Désactiver Mode Invité lors de l'arrivée / Power Notification - Désactiver Mode Invité lors de l'arrivée

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `button_action`: Turn off Mode invité
- `button_title`: Ok!
- `default_message`: Bienvenue à la maison, désactiver le mode invité?
- `default_title`: ✨ Monde Invité
- `discard_when`: Mode invité to “off”
- `persons`: (empty)
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Home

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `button_action` : Désactiver Mode invité
- `button_title` : Ok!
- `default_message` : Bienvenue à la maison, désactiver le mode invité?
- `default_title` : ✨ Monde Invité
- `discard_when` : Mode invité à “off”
- `persons` : (vide)
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Maison
