# Start Escape Game / Start Escape Game

## English
### Steps (high level)
- Set Computed target
- Announce
- Play media
- Generate data
- Pause a target
- Start conversation

```mermaid
flowchart TD
  S["Start"]
  N1["Set Computed target"]
  N2["Announce"]
  N3["Play media"]
  N4["Generate data"]
  N5["Pause a target"]
  N6["Start conversation"]
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
- Définir Cible calculée
- Action : announce
- Action : play media
- Action : generate data
- Pause une cible
- Action : start conversation

```mermaid
flowchart TD
  S["Début"]
  N1["Définir Cible calculée"]
  N2["Action : announce"]
  N3["Action : play media"]
  N4["Action : generate data"]
  N5["Pause une cible"]
  N6["Action : start conversation"]
  E["Fin"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> E
```
