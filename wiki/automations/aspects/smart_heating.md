# Smart Heating / Chauffage intelligent

## English
Heating is managed room-by-room using simple modes, so the home stays comfortable when it’s used and saves energy when it isn’t.

### What you’ll notice
- The **ground floor**, **office**, **bedroom**, **child’s bedroom**, **bathroom**, and **shower room** can each behave differently.
- If a **window/door stays open for a while**, heating for that zone switches to a protective low mode.
- The home may warn about **abnormal temperature** in key rooms.

### Heating modes (concept)
- **Present**: comfort temperature.
- **Absent**: reduced temperature.
- **Frost Guard**: minimum protection temperature (anti-freeze / anti-humidity).
- **Boost** (bathrooms): temporary extra heat, then automatic stop.

### What influences the choice
- The overall home state (Occupied / Empty / Arriving / Leaving).
- Guest Mode (treats the home as occupied for comfort).
- Sleep Mode and Cinema Mode (comfort is kept where it matters).
- Room occupancy detection (for example, when the living area or office is actively used).

### Rules working together
- Pick a heating mode for each main zone (ground floor, office, bedrooms).
- Apply the chosen temperatures for each zone.
- Stop “Boost” automatically after it has run for a while.
- Notify if a room’s temperature becomes abnormal.

Related: [Home Presence Modes](home_presence_modes.md), [Guest Mode](guest_mode.md), [Sleep Mode](sleep_mode.md), [Cinema Mode](cinema_mode.md)

## Français
Le chauffage est géré pièce par pièce avec des modes simples, pour rester confortable quand on utilise une pièce et économiser quand on ne l’utilise pas.

### Ce que vous remarquerez
- Le **rez-de-chaussée**, le **bureau**, la **chambre**, la **chambre enfant**, la **salle de bains** et la **salle de douche** peuvent réagir différemment.
- Si une **porte/fenêtre reste ouverte un moment**, le chauffage de la zone passe en mode de protection (faible).
- La maison peut prévenir en cas de **température anormale** dans certaines pièces.

### Modes de chauffage (principe)
- **Présent** : température de confort.
- **Absent** : température réduite.
- **Frost Guard** : protection minimale (anti-gel / anti-humidité).
- **Boost** (salles d’eau) : chauffe plus fort temporairement, puis arrêt automatique.

### Ce qui influence le choix
- L’état de la maison (Occupée / Vide / Arrivée en cours / Départ en cours).
- Le Mode invité (la maison se comporte comme occupée côté confort).
- Mode sommeil et Mode cinéma (le confort est maintenu là où c’est utile).
- La détection d’occupation des pièces (par exemple, si la pièce de vie ou le bureau est utilisé).

### Règles qui travaillent ensemble
- Choisir un mode de chauffage pour chaque grande zone (rez-de-chaussée, bureau, chambres).
- Appliquer les températures cibles par zone.
- Arrêter automatiquement un “Boost” après une certaine durée.
- Notifier si une température devient anormale dans une pièce.

Liens : [Modes de présence](home_presence_modes.md), [Mode invité](guest_mode.md), [Mode sommeil](sleep_mode.md), [Mode cinéma](cinema_mode.md)

---
Technical details: [Technical page](../technical/aspects/smart_heating.md)
Détails techniques : [Page technique](../technical/aspects/smart_heating.md)
