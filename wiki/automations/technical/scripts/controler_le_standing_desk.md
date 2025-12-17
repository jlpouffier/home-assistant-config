# Controler le Standing desk / Controler le Standing desk

## English
### Steps (high level)
- Branch 1: if A computed rule is true
- Repeat
- Press Standing desk Position 1 (Debout) (Bureau)
- Wait for trigger: Standing desk Mouvement (Bureau) to “on” (timeout 3s)
- Wait for trigger: Standing desk Mouvement (Bureau) to “off” (timeout 20s)
- If A computed rule is true
- Stop
- Branch 2: if A computed rule is true
- Repeat
- Press Standing desk Position 1 (Assis) (Bureau)
- Wait for trigger: Standing desk Mouvement (Bureau) to “on” (timeout 3s)
- Wait for trigger: Standing desk Mouvement (Bureau) to “off” (timeout 20s)
- If A computed rule is true
- Stop

```mermaid
flowchart TD
  S["Start"]
  N1["Branch 1: if A computed rule is true"]
  N2["Repeat"]
  N3["Press Standing desk Position 1 (Debout) (Bureau)"]
  N4["Wait for trigger: Standing desk Mouvement (Bureau) to “on” (timeout 3s)"]
  N5["Wait for trigger: Standing desk Mouvement (Bureau) to “off” (timeout 20s)"]
  N6["If A computed rule is true"]
  N7["Stop"]
  N8["Branch 2: if A computed rule is true"]
  N9["Repeat"]
  N10["Press Standing desk Position 1 (Assis) (Bureau)"]
  N11["Wait for trigger: Standing desk Mouvement (Bureau) to “on” (timeout 3s)"]
  N12["Wait for trigger: Standing desk Mouvement (Bureau) to “off” (timeout 20s)"]
  N13["If A computed rule is true"]
  N14["Stop"]
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
  N12 --> N13
  N13 --> N14
  N14 --> E
```

## Français
### Étapes (niveau simple)
- Branche 1 : si Une règle calculée est vraie
- Répéter
- Appuyer sur Standing desk Position 1 (Debout) (Bureau)
- Attendre le déclencheur : Standing desk Mouvement (Bureau) à “on” (max 3s)
- Attendre le déclencheur : Standing desk Mouvement (Bureau) à “off” (max 20s)
- Si Une règle calculée est vraie
- Arrêter
- Branche 2 : si Une règle calculée est vraie
- Répéter
- Appuyer sur Standing desk Position 1 (Assis) (Bureau)
- Attendre le déclencheur : Standing desk Mouvement (Bureau) à “on” (max 3s)
- Attendre le déclencheur : Standing desk Mouvement (Bureau) à “off” (max 20s)
- Si Une règle calculée est vraie
- Arrêter

```mermaid
flowchart TD
  S["Début"]
  N1["Branche 1 : si Une règle calculée est vraie"]
  N2["Répéter"]
  N3["Appuyer sur Standing desk Position 1 (Debout) (Bureau)"]
  N4["Attendre le déclencheur : Standing desk Mouvement (Bureau) à “on” (max 3s)"]
  N5["Attendre le déclencheur : Standing desk Mouvement (Bureau) à “off” (max 20s)"]
  N6["Si Une règle calculée est vraie"]
  N7["Arrêter"]
  N8["Branche 2 : si Une règle calculée est vraie"]
  N9["Répéter"]
  N10["Appuyer sur Standing desk Position 1 (Assis) (Bureau)"]
  N11["Attendre le déclencheur : Standing desk Mouvement (Bureau) à “on” (max 3s)"]
  N12["Attendre le déclencheur : Standing desk Mouvement (Bureau) à “off” (max 20s)"]
  N13["Si Une règle calculée est vraie"]
  N14["Arrêter"]
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
  N12 --> N13
  N13 --> N14
  N14 --> E
```
