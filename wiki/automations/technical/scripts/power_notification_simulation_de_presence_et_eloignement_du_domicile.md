# Power Notification - Simulation de presence et éloignement du domicile / Power Notification - Simulation de presence et éloignement du domicile

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `button_action`: Turn on Simulation de présence
- `button_title`: D'accord!
- `default_message`: Vous vous trouvez loin du domicile, activer la simulation de présence?
- `default_title`: 🛸 Vous êtes loin
- `discard_when`: Éloignement Domicile to “off”; Simulation de présence to “on”
- `replace_older_notification`: True
- `target`: send_to_nearest
- `thing`: Home

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `button_action` : Activer Simulation de présence
- `button_title` : D'accord!
- `default_message` : Vous vous trouvez loin du domicile, activer la simulation de présence?
- `default_title` : 🛸 Vous êtes loin
- `discard_when` : Éloignement Domicile à “off”; Simulation de présence à “on”
- `replace_older_notification` : True
- `target` : send_to_nearest
- `thing` : Maison
