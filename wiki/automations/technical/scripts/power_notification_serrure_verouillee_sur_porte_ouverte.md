# Power notification - Serrure vérouillée sur porte ouverte / Power notification - Serrure vérouillée sur porte ouverte

## English
- Implemented via blueprint: [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- For the detailed flow (logic, branches, discards), see the blueprint page.

### Inputs used
- `default_importance`: True
- `default_message`: La serrure est verrouillée alors que la porte est toujours ouverte !
- `default_title`: 🔒 Serrure
- `discard_when`: Porte d'entrée (Entrée) to “unlocked”; Porte d'entrée (Entrée) to “off”
- `replace_older_notification`: True
- `target`: send_to_all
- `zones`: Proche de la maison

## Français
- Basé sur le blueprint : [jlo/power_notification_creator.yaml](../blueprints/jlo/power_notification_creator.md)
- Pour le déroulé détaillé (logique, branches, annulations), voir la page du blueprint.

### Entrées utilisées
- `default_importance` : True
- `default_message` : La serrure est verrouillée alors que la porte est toujours ouverte !
- `default_title` : 🔒 Serrure
- `discard_when` : Porte d'entrée (Entrée) à “unlocked”; Porte d'entrée (Entrée) à “off”
- `replace_older_notification` : True
- `target` : send_to_all
- `zones` : Proche de la maison
