# Power Notification - Pluie et portes ouvertes / Power Notification - Pluie et portes ouvertes

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `default_message`: Certaines portes sont ouvertes et il commence a pleuvoir
- `default_title`: 🌂 In pleut!
- `discard_when`: Toutes les portes to “off”; Station météo Pluie (Jardin) to “0.0”
- `replace_older_notification`: True
- `target`: send_to_persons_in_zones
- `zones`: Home

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `default_message` : Certaines portes sont ouvertes et il commence a pleuvoir
- `default_title` : 🌂 In pleut!
- `discard_when` : Toutes les portes à “off”; Station météo Pluie (Jardin) à “0.0”
- `replace_older_notification` : True
- `target` : send_to_persons_in_zones
- `zones` : Maison
