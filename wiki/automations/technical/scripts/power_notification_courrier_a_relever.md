# Power Notification - Courrier à relever / Power Notification - Courrier à relever

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `button_action`: Turn off Courrier à relever (Rue)
- `button_title`: Courrier relevé!
- `default_message`: Vous avez du courrier !
- `default_title`: 📫 Boite aux lettres
- `discard_when`: Courrier à relever (Rue) to “off”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Home

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `button_action` : Désactiver Courrier à relever (Rue)
- `button_title` : Courrier relevé!
- `default_message` : Vous avez du courrier !
- `default_title` : 📫 Boite aux lettres
- `discard_when` : Courrier à relever (Rue) à “off”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Maison
