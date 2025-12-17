# Clignoter le bureau / Clignoter le bureau

## English
### Steps (high level)
- Turn on Bureau central (Bureau)
- Wait 0s
- Turn off Bureau central (Bureau)
- Wait 1s
- Turn on Bureau central (Bureau)

```mermaid
flowchart TD
  S["Start"]
  N1["Turn on Bureau central (Bureau)"]
  N2["Wait 0s"]
  N3["Turn off Bureau central (Bureau)"]
  N4["Wait 1s"]
  N5["Turn on Bureau central (Bureau)"]
  E["End"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> E
```

## Français
### Étapes (niveau simple)
- Allumer Bureau central (Bureau)
- Attendre 0s
- Éteindre Bureau central (Bureau)
- Attendre 1s
- Allumer Bureau central (Bureau)

```mermaid
flowchart TD
  S["Début"]
  N1["Allumer Bureau central (Bureau)"]
  N2["Attendre 0s"]
  N3["Éteindre Bureau central (Bureau)"]
  N4["Attendre 1s"]
  N5["Allumer Bureau central (Bureau)"]
  E["Fin"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> E
```
