# Réveil Lumineux - Musique / Réveil Lumineux - Musique

## English
### Steps (high level)
- Adjust volume
- Shuffle set Enceintes (Chambre)
- Play media Enceintes (Chambre)
- Wait 10s
- If NOT (Enceintes (Chambre) is “playing”)
- Play Enceintes (Chambre)
- Wait 10s
- If NOT (Enceintes (Chambre) is “playing”)
- Media next track Enceintes (Chambre)

```mermaid
flowchart TD
  S["Start"]
  N1["Adjust volume"]
  N2["Shuffle set Enceintes (Chambre)"]
  N3["Play media Enceintes (Chambre)"]
  N4["Wait 10s"]
  N5["If NOT (Enceintes (Chambre) is “playing”)"]
  N6["Play Enceintes (Chambre)"]
  N7["Wait 10s"]
  N8["If NOT (Enceintes (Chambre) is “playing”)"]
  N9["Media next track Enceintes (Chambre)"]
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
  N9 --> E
```

## Français
### Étapes (niveau simple)
- Régler le volume
- Action : shuffle set sur Enceintes (Chambre)
- Action : play media sur Enceintes (Chambre)
- Attendre 10s
- Si NON (Enceintes (Chambre) est “playing”)
- Lecture Enceintes (Chambre)
- Attendre 10s
- Si NON (Enceintes (Chambre) est “playing”)
- Action : media next track sur Enceintes (Chambre)

```mermaid
flowchart TD
  S["Début"]
  N1["Régler le volume"]
  N2["Action : shuffle set sur Enceintes (Chambre)"]
  N3["Action : play media sur Enceintes (Chambre)"]
  N4["Attendre 10s"]
  N5["Si NON (Enceintes (Chambre) est “playing”)"]
  N6["Lecture Enceintes (Chambre)"]
  N7["Attendre 10s"]
  N8["Si NON (Enceintes (Chambre) est “playing”)"]
  N9["Action : media next track sur Enceintes (Chambre)"]
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
  N9 --> E
```
