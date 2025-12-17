# Éteindre tous les lecteurs multimédia / Éteindre tous les lecteurs multimédia

## English
### Steps (high level)
- Pause Tous les lecteurs multimédia (Ne supportant pas On/Off)
- Turn off Tous les lecteurs multimédia (supportant On/Off)
- Turn off TV (Salon)

```mermaid
flowchart TD
  S["Start"]
  N1["Pause Tous les lecteurs multimédia (Ne supportant pas On/Off)"]
  N2["Turn off Tous les lecteurs multimédia (supportant On/Off)"]
  N3["Turn off TV (Salon)"]
  E["End"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> E
```

## Français
### Étapes (niveau simple)
- Pause Tous les lecteurs multimédia (Ne supportant pas On/Off)
- Éteindre Tous les lecteurs multimédia (supportant On/Off)
- Éteindre TV (Salon)

```mermaid
flowchart TD
  S["Début"]
  N1["Pause Tous les lecteurs multimédia (Ne supportant pas On/Off)"]
  N2["Éteindre Tous les lecteurs multimédia (supportant On/Off)"]
  N3["Éteindre TV (Salon)"]
  E["Fin"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> E
```
