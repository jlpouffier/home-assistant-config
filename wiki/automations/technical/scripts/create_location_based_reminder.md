# Create Location Based Reminder / Create Location Based Reminder

## English
### Flow (trace-style)
- Entry: when this script is run
- CHOOSE (first match)
  - Branch 1
    - Check: A custom rule is true
    - THEN
      - Add item Rappels Maison Vide
  - Branch 2
    - Check: A custom rule is true
    - THEN
      - Add item Rappels Maison Occupée

## Français
### Déroulé (style ‘trace’)
- Entrée : quand ce script est exécuté
- CHOISIR (première branche valide)
  - Branche 1
    - Vérifier : Une règle personnalisée est vraie
    - ALORS
      - Action : add item sur Rappels Maison Vide
  - Branche 2
    - Vérifier : Une règle personnalisée est vraie
    - ALORS
      - Action : add item sur Rappels Maison Occupée
