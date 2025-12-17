# Éteindre et Sécuriser la maison / Éteindre et Sécuriser la maison

## English
### Flow (trace-style)
- Entry: when this script is run
- Turn off Assistants vocaux
- Run script: Éteindre tous les lecteurs multimédia
- IF
  - Check: Mode Chien is “off”
  - Check: Simulation de présence is “off”
  - THEN
    - Turn off Toutes les Lumières
    - Close shutters
      - IF
        - Check: Surveillance de la maison - Fermer le volet quand maison vide is “on”
        - THEN
          - Close Volets (Salon)
- Lock door
  - IF
    - Check: Porte d'entrée (Entrée) is “off”
    - THEN
      - Wait 1s
      - Lock Porte d'entrée (Entrée)
    - ELSE
      - Run script: Power Notification - Porte d'entrée ouverte lors du départ

### Scripts called
- [Éteindre tous les lecteurs multimédia](eteindre_tous_les_lecteur_multimedia.md)
- [Power Notification - Porte d'entrée ouverte lors du départ](power_notification_porte_d_entree_ouverte.md)

## Français
### Déroulé (style ‘trace’)
- Entrée : quand ce script est exécuté
- Éteindre Assistants vocaux
- Lancer le script : Éteindre tous les lecteurs multimédia
- SI
  - Vérifier : Mode Chien est “off”
  - Vérifier : Simulation de présence est “off”
  - ALORS
    - Éteindre Toutes les Lumières
    - Close shutters
      - SI
        - Vérifier : Surveillance de la maison - Fermer le volet quand maison vide est “on”
        - ALORS
          - Fermer Volets (Salon)
- Lock door
  - SI
    - Vérifier : Porte d'entrée (Entrée) est “off”
    - ALORS
      - Attendre 1s
      - Verrouiller Porte d'entrée (Entrée)
    - SINON
      - Lancer le script : Power Notification - Porte d'entrée ouverte lors du départ

### Scripts appelés
- [Éteindre tous les lecteurs multimédia](eteindre_tous_les_lecteur_multimedia.md)
- [Power Notification - Porte d'entrée ouverte lors du départ](power_notification_porte_d_entree_ouverte.md)
