# Préparer départ maison / Préparer départ maison

## English
### Steps (high level)
- If Toutes les fenêtres is “on”
- Run script: Power Notification - Fenêtres ouvertes
- If Four En cours d'utilisation (Cuisine) is “on”
- Run script: Power Notification - Four allumé
- If Plaques à induction En cours d'utilisation (Cuisine) is “on”
- Run script: Power Notification - Plaques à induction allumées
- If Porte fenêtre (Salon) is “on”
- Run script: Power Notification - Porte fenêtre du salon ouverte
- If Porte Réfrigérateur (Cuisine) is “on”
- Run script: Power Notification - Porte réfrigérateur restée ouverte
- If Porte Congélateur (Cuisine) is “on”
- Run script: Power Notification - Porte congélateur restée ouverte

### Scripts called
- [Power Notification - Fenêtres ouvertes](power_notification_fenetres_ouvertes.md)
- [Power Notification - Four allumé](power_notification_four_allume.md)
- [Power Notification - Plaques à induction allumées](power_notification_plaques_a_induction_allumees.md)
- [Power Notification - Porte congélateur restée ouverte](power_notification_porte_congelateur_restee_ouverte.md)
- [Power Notification - Porte fenêtre du salon ouverte](power_notification_porte_fenetre_du_salon_ouverte.md)
- [Power Notification - Porte réfrigérateur restée ouverte](power_notification_porte_refrigerateur_restee_ouverte.md)

```mermaid
flowchart TD
  S["Start"]
  N1["If Toutes les fenêtres is “on”"]
  N2["Run script: Power Notification - Fenêtres ouvertes"]
  N3["If Four En cours d'utilisation (Cuisine) is “on”"]
  N4["Run script: Power Notification - Four allumé"]
  N5["If Plaques à induction En cours d'utilisation (Cuisine) is “on”"]
  N6["Run script: Power Notification - Plaques à induction allumées"]
  N7["If Porte fenêtre (Salon) is “on”"]
  N8["Run script: Power Notification - Porte fenêtre du salon ouverte"]
  N9["If Porte Réfrigérateur (Cuisine) is “on”"]
  N10["Run script: Power Notification - Porte réfrigérateur restée ouverte"]
  N11["If Porte Congélateur (Cuisine) is “on”"]
  N12["Run script: Power Notification - Porte congélateur restée ouverte"]
  E["End"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> N7
  N7 --> N8
  N8 --> N9
  N9 --> N10
  N10 --> N11
  N11 --> N12
  N12 --> E
```

## Français
### Étapes (niveau simple)
- Si Toutes les fenêtres est “on”
- Lancer le script : Power Notification - Fenêtres ouvertes
- Si Four En cours d'utilisation (Cuisine) est “on”
- Lancer le script : Power Notification - Four allumé
- Si Plaques à induction En cours d'utilisation (Cuisine) est “on”
- Lancer le script : Power Notification - Plaques à induction allumées
- Si Porte fenêtre (Salon) est “on”
- Lancer le script : Power Notification - Porte fenêtre du salon ouverte
- Si Porte Réfrigérateur (Cuisine) est “on”
- Lancer le script : Power Notification - Porte réfrigérateur restée ouverte
- Si Porte Congélateur (Cuisine) est “on”
- Lancer le script : Power Notification - Porte congélateur restée ouverte

### Scripts appelés
- [Power Notification - Fenêtres ouvertes](power_notification_fenetres_ouvertes.md)
- [Power Notification - Four allumé](power_notification_four_allume.md)
- [Power Notification - Plaques à induction allumées](power_notification_plaques_a_induction_allumees.md)
- [Power Notification - Porte congélateur restée ouverte](power_notification_porte_congelateur_restee_ouverte.md)
- [Power Notification - Porte fenêtre du salon ouverte](power_notification_porte_fenetre_du_salon_ouverte.md)
- [Power Notification - Porte réfrigérateur restée ouverte](power_notification_porte_refrigerateur_restee_ouverte.md)

```mermaid
flowchart TD
  S["Début"]
  N1["Si Toutes les fenêtres est “on”"]
  N2["Lancer le script : Power Notification - Fenêtres ouvertes"]
  N3["Si Four En cours d'utilisation (Cuisine) est “on”"]
  N4["Lancer le script : Power Notification - Four allumé"]
  N5["Si Plaques à induction En cours d'utilisation (Cuisine) est “on”"]
  N6["Lancer le script : Power Notification - Plaques à induction allumées"]
  N7["Si Porte fenêtre (Salon) est “on”"]
  N8["Lancer le script : Power Notification - Porte fenêtre du salon ouverte"]
  N9["Si Porte Réfrigérateur (Cuisine) est “on”"]
  N10["Lancer le script : Power Notification - Porte réfrigérateur restée ouverte"]
  N11["Si Porte Congélateur (Cuisine) est “on”"]
  N12["Lancer le script : Power Notification - Porte congélateur restée ouverte"]
  E["Fin"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> N7
  N7 --> N8
  N8 --> N9
  N9 --> N10
  N10 --> N11
  N11 --> N12
  N12 --> E
```
