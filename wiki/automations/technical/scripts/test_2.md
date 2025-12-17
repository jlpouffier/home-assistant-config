# Crazy Wake Up / Crazy Wake Up

## English
### Steps (high level)
- Adjust volume
- Play media Assistant vocal Lecteur multimédia (Chambre)
- Wait for trigger: Assistant vocal Lecteur multimédia (Chambre) to “playing”
- Turn on a target
- Wait 12s
- Turn off a target
- Wait 2s
- Repeat
- Turn on Lumières (Chambre)
- Wait 1s

```mermaid
flowchart TD
  S["Start"]
  N1["Adjust volume"]
  N2["Play media Assistant vocal Lecteur multimédia (Chambre)"]
  N3["Wait for trigger: Assistant vocal Lecteur multimédia (Chambre) to “playing”"]
  N4["Turn on a target"]
  N5["Wait 12s"]
  N6["Turn off a target"]
  N7["Wait 2s"]
  N8["Repeat"]
  N9["Turn on Lumières (Chambre)"]
  N10["Wait 1s"]
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
  N10 --> E
```

## Français
### Étapes (niveau simple)
- Régler le volume
- Action : play media sur Assistant vocal Lecteur multimédia (Chambre)
- Attendre le déclencheur : Assistant vocal Lecteur multimédia (Chambre) à “playing”
- Allumer une cible
- Attendre 12s
- Éteindre une cible
- Attendre 2s
- Répéter
- Allumer Lumières (Chambre)
- Attendre 1s

```mermaid
flowchart TD
  S["Début"]
  N1["Régler le volume"]
  N2["Action : play media sur Assistant vocal Lecteur multimédia (Chambre)"]
  N3["Attendre le déclencheur : Assistant vocal Lecteur multimédia (Chambre) à “playing”"]
  N4["Allumer une cible"]
  N5["Attendre 12s"]
  N6["Éteindre une cible"]
  N7["Attendre 2s"]
  N8["Répéter"]
  N9["Allumer Lumières (Chambre)"]
  N10["Attendre 1s"]
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
  N10 --> E
```
