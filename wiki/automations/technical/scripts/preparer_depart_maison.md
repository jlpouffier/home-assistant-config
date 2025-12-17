# Préparer départ maison / Préparer départ maison

## English
### Flow (trace-style)
- Entry: when this script is run
- Notify windows open
  - IF
    - Check: Toutes les fenêtres is “on”
    - THEN
      - Run script: Power Notification - Fenêtres ouvertes
- Notify oven running
  - IF
    - Check: Four En cours d'utilisation (Cuisine) is “on”
    - THEN
      - Run script: Power Notification - Four allumé
- Notify cooktop running
  - IF
    - Check: Plaques à induction En cours d'utilisation (Cuisine) is “on”
    - THEN
      - Run script: Power Notification - Plaques à induction allumées
- Notify french door open
  - IF
    - Check: Porte fenêtre (Salon) is “on”
    - THEN
      - Run script: Power Notification - Porte fenêtre du salon ouverte
- Notify top fridge door open
  - IF
    - Check: Porte Réfrigérateur (Cuisine) is “on”
    - THEN
      - Run script: Power Notification - Porte réfrigérateur restée ouverte
- Notify bottom fridge door open
  - IF
    - Check: Porte Congélateur (Cuisine) is “on”
    - THEN
      - Run script: Power Notification - Porte congélateur restée ouverte

### Scripts called
- [Power Notification - Fenêtres ouvertes](power_notification_fenetres_ouvertes.md)
- [Power Notification - Four allumé](power_notification_four_allume.md)
- [Power Notification - Plaques à induction allumées](power_notification_plaques_a_induction_allumees.md)
- [Power Notification - Porte congélateur restée ouverte](power_notification_porte_congelateur_restee_ouverte.md)
- [Power Notification - Porte fenêtre du salon ouverte](power_notification_porte_fenetre_du_salon_ouverte.md)
- [Power Notification - Porte réfrigérateur restée ouverte](power_notification_porte_refrigerateur_restee_ouverte.md)

## Français
### Déroulé (style ‘trace’)
- Entrée : quand ce script est exécuté
- Notify windows open
  - SI
    - Vérifier : Toutes les fenêtres est “on”
    - ALORS
      - Lancer le script : Power Notification - Fenêtres ouvertes
- Notify oven running
  - SI
    - Vérifier : Four En cours d'utilisation (Cuisine) est “on”
    - ALORS
      - Lancer le script : Power Notification - Four allumé
- Notify cooktop running
  - SI
    - Vérifier : Plaques à induction En cours d'utilisation (Cuisine) est “on”
    - ALORS
      - Lancer le script : Power Notification - Plaques à induction allumées
- Notify french door open
  - SI
    - Vérifier : Porte fenêtre (Salon) est “on”
    - ALORS
      - Lancer le script : Power Notification - Porte fenêtre du salon ouverte
- Notify top fridge door open
  - SI
    - Vérifier : Porte Réfrigérateur (Cuisine) est “on”
    - ALORS
      - Lancer le script : Power Notification - Porte réfrigérateur restée ouverte
- Notify bottom fridge door open
  - SI
    - Vérifier : Porte Congélateur (Cuisine) est “on”
    - ALORS
      - Lancer le script : Power Notification - Porte congélateur restée ouverte

### Scripts appelés
- [Power Notification - Fenêtres ouvertes](power_notification_fenetres_ouvertes.md)
- [Power Notification - Four allumé](power_notification_four_allume.md)
- [Power Notification - Plaques à induction allumées](power_notification_plaques_a_induction_allumees.md)
- [Power Notification - Porte congélateur restée ouverte](power_notification_porte_congelateur_restee_ouverte.md)
- [Power Notification - Porte fenêtre du salon ouverte](power_notification_porte_fenetre_du_salon_ouverte.md)
- [Power Notification - Porte réfrigérateur restée ouverte](power_notification_porte_refrigerateur_restee_ouverte.md)
