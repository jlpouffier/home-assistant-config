# Jouer de la musique (Music Assistant) / Jouer de la musique (Music Assistant)

## English
### Steps (high level)
- Process
- Generate data
- Branch 1: if A computed rule is true
- Play media
- Play media
- Branch 2: if A computed rule is true
- Play media
- Stop

```mermaid
flowchart TD
  S["Start"]
  N1["Process"]
  N2["Generate data"]
  N3["Branch 1: if A computed rule is true"]
  N4["Play media"]
  N5["Play media"]
  N6["Branch 2: if A computed rule is true"]
  N7["Play media"]
  N8["Stop"]
  E["End"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> N7
  N7 --> N8
  N8 --> E
```

## Français
### Étapes (niveau simple)
- Action : process
- Action : generate data
- Branche 1 : si Une règle calculée est vraie
- Action : play media
- Action : play media
- Branche 2 : si Une règle calculée est vraie
- Action : play media
- Arrêter

```mermaid
flowchart TD
  S["Début"]
  N1["Action : process"]
  N2["Action : generate data"]
  N3["Branche 1 : si Une règle calculée est vraie"]
  N4["Action : play media"]
  N5["Action : play media"]
  N6["Branche 2 : si Une règle calculée est vraie"]
  N7["Action : play media"]
  N8["Arrêter"]
  E["Fin"]
  S --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> N7
  N7 --> N8
  N8 --> E
```
