# Controler le Standing desk / Controler le Standing desk

## English
### Flow (trace-style)
- Entry: when this script is run
- CHOOSE (first match)
  - Branch 1
    - Check: A custom rule is true
    - THEN
      - REPEAT
        - Press Standing desk Position 1 (Debout) (Bureau)
        - Wait for: Standing desk Mouvement (Bureau) to “on” (timeout 3s)
        - Wait for: Standing desk Mouvement (Bureau) to “off” (timeout 20s)
        - IF
          - Check: A custom rule is true
          - THEN
            - Stop
  - Branch 2
    - Check: A custom rule is true
    - THEN
      - REPEAT
        - Press Standing desk Position 1 (Assis) (Bureau)
        - Wait for: Standing desk Mouvement (Bureau) to “on” (timeout 3s)
        - Wait for: Standing desk Mouvement (Bureau) to “off” (timeout 20s)
        - IF
          - Check: A custom rule is true
          - THEN
            - Stop

## Français
### Déroulé (style ‘trace’)
- Entrée : quand ce script est exécuté
- CHOISIR (première branche valide)
  - Branche 1
    - Vérifier : Une règle personnalisée est vraie
    - ALORS
      - RÉPÉTER
        - Appuyer sur Standing desk Position 1 (Debout) (Bureau)
        - Attendre : Standing desk Mouvement (Bureau) à “on” (max 3s)
        - Attendre : Standing desk Mouvement (Bureau) à “off” (max 20s)
        - SI
          - Vérifier : Une règle personnalisée est vraie
          - ALORS
            - Arrêter
  - Branche 2
    - Vérifier : Une règle personnalisée est vraie
    - ALORS
      - RÉPÉTER
        - Appuyer sur Standing desk Position 1 (Assis) (Bureau)
        - Attendre : Standing desk Mouvement (Bureau) à “on” (max 3s)
        - Attendre : Standing desk Mouvement (Bureau) à “off” (max 20s)
        - SI
          - Vérifier : Une règle personnalisée est vraie
          - ALORS
            - Arrêter
