# Démarrer la routine du sommeil de Child / Démarrer la routine du sommeil de Enfant

## English
### Steps (high level)
- Adjust volume
- Play media Enceintes (Chambre de Child)
- Shuffle set Enceintes (Chambre de Child)
- Wait 10s
- If NOT (Enceintes (Chambre de Child) is “playing”)
- Play Enceintes (Chambre de Child)
- Wait 10s
- If NOT (Enceintes (Chambre de Child) is “playing”)
- Media next track Enceintes (Chambre de Child)

```mermaid
flowchart TD
  S["Start"]
  N1["Adjust volume"]
  N2["Play media Enceintes (Chambre de Child)"]
  N3["Shuffle set Enceintes (Chambre de Child)"]
  N4["Wait 10s"]
  N5["If NOT (Enceintes (Chambre de Child) is “playing”)"]
  N6["Play Enceintes (Chambre de Child)"]
  N7["Wait 10s"]
  N8["If NOT (Enceintes (Chambre de Child) is “playing”)"]
  N9["Media next track Enceintes (Chambre de Child)"]
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
- Action : play media sur Enceintes (Chambre de Enfant)
- Action : shuffle set sur Enceintes (Chambre de Enfant)
- Attendre 10s
- Si NON (Enceintes (Chambre de Enfant) est “playing”)
- Lecture Enceintes (Chambre de Enfant)
- Attendre 10s
- Si NON (Enceintes (Chambre de Enfant) est “playing”)
- Action : media next track sur Enceintes (Chambre de Enfant)

```mermaid
flowchart TD
  S["Début"]
  N1["Régler le volume"]
  N2["Action : play media sur Enceintes (Chambre de Enfant)"]
  N3["Action : shuffle set sur Enceintes (Chambre de Enfant)"]
  N4["Attendre 10s"]
  N5["Si NON (Enceintes (Chambre de Enfant) est “playing”)"]
  N6["Lecture Enceintes (Chambre de Enfant)"]
  N7["Attendre 10s"]
  N8["Si NON (Enceintes (Chambre de Enfant) est “playing”)"]
  N9["Action : media next track sur Enceintes (Chambre de Enfant)"]
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
