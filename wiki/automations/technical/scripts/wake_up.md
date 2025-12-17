# Réveil Lumineux - Lumières / Réveil Lumineux - Lumières

## English
### Steps (high level)
- Turn off a target
- Turn on Bloom (Chambre)
- Wait 5m
- Turn on Suspension (Chambre), Lampe de chevet droite (Chambre), Lampe de chevet gauche (Chambre)
- Wait 10m
- Turn on Guirlande (Chambre)

```mermaid
flowchart TD
  S["Start"]
  N1["Turn off a target"]
  N2["Turn on Bloom (Chambre)"]
  N3["Wait 5m"]
  N4["Turn on Suspension (Chambre), Lampe de chevet droite (Chambre), Lampe de chevet gauche (Chambre)"]
  N5["Wait 10m"]
  N6["Turn on Guirlande (Chambre)"]
  E["End"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> E
```

## Français
### Étapes (niveau simple)
- Éteindre une cible
- Allumer Bloom (Chambre)
- Attendre 5m
- Allumer Suspension (Chambre), Lampe de chevet droite (Chambre), Lampe de chevet gauche (Chambre)
- Attendre 10m
- Allumer Guirlande (Chambre)

```mermaid
flowchart TD
  S["Début"]
  N1["Éteindre une cible"]
  N2["Allumer Bloom (Chambre)"]
  N3["Attendre 5m"]
  N4["Allumer Suspension (Chambre), Lampe de chevet droite (Chambre), Lampe de chevet gauche (Chambre)"]
  N5["Attendre 10m"]
  N6["Allumer Guirlande (Chambre)"]
  E["Fin"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> E
```
