# Create Location Based Reminder / Create Location Based Reminder

## English
### Steps (high level)
- Branch 1: if A computed rule is true
- Add item Rappels Maison Vide
- Branch 2: if A computed rule is true
- Add item Rappels Maison Occupée

```mermaid
flowchart TD
  S["Start"]
  N1["Branch 1: if A computed rule is true"]
  N2["Add item Rappels Maison Vide"]
  N3["Branch 2: if A computed rule is true"]
  N4["Add item Rappels Maison Occupée"]
  E["End"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> E
```

## Français
### Étapes (niveau simple)
- Branche 1 : si Une règle calculée est vraie
- Action : add item sur Rappels Maison Vide
- Branche 2 : si Une règle calculée est vraie
- Action : add item sur Rappels Maison Occupée

```mermaid
flowchart TD
  S["Début"]
  N1["Branche 1 : si Une règle calculée est vraie"]
  N2["Action : add item sur Rappels Maison Vide"]
  N3["Branche 2 : si Une règle calculée est vraie"]
  N4["Action : add item sur Rappels Maison Occupée"]
  E["Fin"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> E
```
