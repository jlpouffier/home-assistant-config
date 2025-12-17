# Démarrer la routine du sommeil de Child / Démarrer la routine du sommeil de Enfant

## English
### Flow (trace-style)
- Entry: when this script is run
- Adjust volume
- Play media
- Shuffle set Enceintes (Chambre de Child)
- Fallback in case audio does not start
  - Wait 10s
  - IF
    - Check: NOT (Enceintes (Chambre de Child) is “playing”)
    - THEN
      - Play Enceintes (Chambre de Child)
      - Wait 10s
      - IF
        - Check: NOT (Enceintes (Chambre de Child) is “playing”)
        - THEN
          - Media next track Enceintes (Chambre de Child)

## Français
### Déroulé (style ‘trace’)
- Entrée : quand ce script est exécuté
- Régler le volume
- Lancer un média
- Action : shuffle set sur Enceintes (Chambre de Enfant)
- Fallback in case audio does not start
  - Attendre 10s
  - SI
    - Vérifier : NON (Enceintes (Chambre de Enfant) est “playing”)
    - ALORS
      - Lecture Enceintes (Chambre de Enfant)
      - Attendre 10s
      - SI
        - Vérifier : NON (Enceintes (Chambre de Enfant) est “playing”)
        - ALORS
          - Action : media next track sur Enceintes (Chambre de Enfant)
