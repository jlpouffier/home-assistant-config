# Réveil Lumineux - Musique / Réveil Lumineux - Musique

## English
### Flow (trace-style)
- Entry: when this script is run
- Adjust volume
- Shuffle set Enceintes (Chambre)
- Play media
- Fallback in case audio does not start
  - Wait 10s
  - IF
    - Check: NOT (Enceintes (Chambre) is “playing”)
    - THEN
      - Play Enceintes (Chambre)
      - Wait 10s
      - IF
        - Check: NOT (Enceintes (Chambre) is “playing”)
        - THEN
          - Media next track Enceintes (Chambre)

## Français
### Déroulé (style ‘trace’)
- Entrée : quand ce script est exécuté
- Régler le volume
- Action : shuffle set sur Enceintes (Chambre)
- Lancer un média
- Fallback in case audio does not start
  - Attendre 10s
  - SI
    - Vérifier : NON (Enceintes (Chambre) est “playing”)
    - ALORS
      - Lecture Enceintes (Chambre)
      - Attendre 10s
      - SI
        - Vérifier : NON (Enceintes (Chambre) est “playing”)
        - ALORS
          - Action : media next track sur Enceintes (Chambre)
