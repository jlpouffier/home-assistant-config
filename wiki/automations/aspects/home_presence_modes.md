# Home Presence Modes / Modes de présence de la maison

## English
The house maintains a simple “home state” that many other automations depend on (heating/AC, alerts, arrival/departure routines).

### The 4 states
- **Occupied**: at least one person is at home.
- **Empty**: nobody is at home.
- **Arriving**: someone is in the process of coming home (used to prepare a smooth arrival).
- **Leaving**: someone is in the process of leaving (used to avoid false alerts while the door is being used).

### What you’ll notice
- When someone arrives, some devices may turn on automatically (comfort / visibility).
- When the home becomes empty, some devices may turn off, and the alarm may arm.
- The system tries to be forgiving: it distinguishes “in transit” from “fully gone”.

### How it decides (high level)
- **Front door activity** can switch the home to **Occupied** or confirm **Empty** after the door closes.
- **Occupancy detection** can start **Arriving** (if the home was Empty) or **Leaving** (if the home was Occupied).
- **The alarm** arming/disarming also helps confirm “leaving” or “arriving”.
- **Voice command (French)** can start **Leaving** from inside the home (see [Voice Commands](voice_commands.md)).

### Rules working together
- Set **Occupied** when the front door opens.
- If the home is in **Leaving**, wait for the door to close, then set **Empty**.
- If occupancy is detected while **Empty**, switch to **Arriving**.
- If occupancy disappears while **Occupied/Arriving**, switch to **Leaving**.

Related: [Guest Mode](guest_mode.md), [Home Security & Safety](home_security_and_safety.md), [Smart Heating](smart_heating.md), [Smart Air Conditioning](smart_air_conditioning.md)

## Français
La maison maintient un “mode de présence” simple, dont dépendent beaucoup d’automatismes (chauffage/clim, alertes, routines arrivée/départ).

### Les 4 états
- **Occupée** : au moins une personne est à la maison.
- **Vide** : personne à la maison.
- **Arrivée en cours** : une arrivée est en train de se produire (pour préparer l’accueil).
- **Départ en cours** : un départ est en train de se produire (pour éviter les fausses alertes pendant l’usage de la porte).

### Ce que vous remarquerez
- À l’arrivée, certains appareils peuvent s’allumer automatiquement (confort / visibilité).
- Quand la maison devient vide, certains appareils peuvent s’éteindre et l’alarme peut s’armer.
- Le système distingue “en cours” de “effectivement parti” afin d’éviter des comportements brusques.

### Comment ça décide (niveau simple)
- **La porte d’entrée** peut faire passer la maison en **Occupée** ou confirmer **Vide** après fermeture.
- **La détection de présence** peut lancer **Arrivée en cours** (si la maison était vide) ou **Départ en cours** (si elle était occupée).
- **L’alarme** (armement/désarmement) aide aussi à confirmer arrivée/départ.
- **Une phrase vocale** (en français) peut lancer **Départ en cours** depuis l’intérieur (voir [Commandes vocales](voice_commands.md)).

### Règles qui travaillent ensemble
- Mettre **Occupée** quand la porte d’entrée s’ouvre.
- Si la maison est en **Départ en cours**, attendre la fermeture puis mettre **Vide**.
- Si une présence est détectée alors que la maison est **Vide**, passer en **Arrivée en cours**.
- Si la présence disparaît alors que la maison est **Occupée/Arrivée en cours**, passer en **Départ en cours**.

Liens : [Mode invité](guest_mode.md), [Sécurité & sûreté](home_security_and_safety.md), [Chauffage intelligent](smart_heating.md), [Climatisation intelligente](smart_air_conditioning.md)

---
Technical details: [Technical page](../technical/aspects/home_presence_modes.md)
Détails techniques : [Page technique](../technical/aspects/home_presence_modes.md)
