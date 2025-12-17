# Éteindre et Sécuriser la maison / Éteindre et Sécuriser la maison

## English
### Steps (high level)
- Turn off Assistants vocaux
- Run script: Éteindre tous les lecteurs multimédia
- If Mode Chien is “off”
- And Simulation de présence is “off”
- Turn off Toutes les Lumières
- If Surveillance de la maison - Fermer le volet quand maison vide is “on”
- Close Volets (Salon)
- If Porte d'entrée (Entrée) is “off”
- Wait 1s
- Lock Porte d'entrée (Entrée)
- Else
- Run script: Power Notification - Porte d'entrée ouverte lors du départ

### Scripts called
- [Éteindre tous les lecteurs multimédia](eteindre_tous_les_lecteur_multimedia.md)
- [Power Notification - Porte d'entrée ouverte lors du départ](power_notification_porte_d_entree_ouverte.md)

```mermaid
flowchart TD
  S["Start"]
  N1["Turn off Assistants vocaux"]
  N2["Run script: Éteindre tous les lecteurs multimédia"]
  N3["If Mode Chien is “off”"]
  N4["And Simulation de présence is “off”"]
  N5["Turn off Toutes les Lumières"]
  N6["If Surveillance de la maison - Fermer le volet quand maison vide is “on”"]
  N7["Close Volets (Salon)"]
  N8["If Porte d'entrée (Entrée) is “off”"]
  N9["Wait 1s"]
  N10["Lock Porte d'entrée (Entrée)"]
  N11["Else"]
  N12["Run script: Power Notification - Porte d'entrée ouverte lors du départ"]
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
- Éteindre Assistants vocaux
- Lancer le script : Éteindre tous les lecteurs multimédia
- Si Mode Chien est “off”
- Et Simulation de présence est “off”
- Éteindre Toutes les Lumières
- Si Surveillance de la maison - Fermer le volet quand maison vide est “on”
- Fermer Volets (Salon)
- Si Porte d'entrée (Entrée) est “off”
- Attendre 1s
- Verrouiller Porte d'entrée (Entrée)
- Sinon
- Lancer le script : Power Notification - Porte d'entrée ouverte lors du départ

### Scripts appelés
- [Éteindre tous les lecteurs multimédia](eteindre_tous_les_lecteur_multimedia.md)
- [Power Notification - Porte d'entrée ouverte lors du départ](power_notification_porte_d_entree_ouverte.md)

```mermaid
flowchart TD
  S["Début"]
  N1["Éteindre Assistants vocaux"]
  N2["Lancer le script : Éteindre tous les lecteurs multimédia"]
  N3["Si Mode Chien est “off”"]
  N4["Et Simulation de présence est “off”"]
  N5["Éteindre Toutes les Lumières"]
  N6["Si Surveillance de la maison - Fermer le volet quand maison vide est “on”"]
  N7["Fermer Volets (Salon)"]
  N8["Si Porte d'entrée (Entrée) est “off”"]
  N9["Attendre 1s"]
  N10["Verrouiller Porte d'entrée (Entrée)"]
  N11["Sinon"]
  N12["Lancer le script : Power Notification - Porte d'entrée ouverte lors du départ"]
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
