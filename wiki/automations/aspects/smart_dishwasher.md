# Smart Dishwasher / Lave-vaisselle

## English
The dishwasher is tracked with a simple status so the home can schedule, remind, and avoid unnecessary noise.

### What you’ll notice
- The dishwasher can be **scheduled at night**.
- You may get a notification when a cycle is **planned**, **finished**, or when it’s **ready to be emptied**.
- If a cycle is cancelled mid-way, the home can reset the status.

### Status (concept)
- **Inactive** → **Planned** → **Washing in progress** → **To empty** → back to **Inactive**

### Rules working together
- Schedule a wash at night.
- Keep the dishwasher “status” in sync (planned / running / to empty).
- Notify at key moments (start planned, cycle finished, time to empty).
- Reset status if a wash is cancelled.

Related: [Voice Commands](voice_commands.md)

## Français
Le lave-vaisselle est suivi via un état simple pour planifier, rappeler, et éviter du bruit inutile.

### Ce que vous remarquerez
- Le lave-vaisselle peut être **planifié la nuit**.
- Une notification peut prévenir quand un cycle est **planifié**, **terminé**, ou quand il est **à vider**.
- En cas d’annulation, l’état peut être réinitialisé.

### États (principe)
- **Inactif** → **Planifié** → **Lavage en cours** → **À vider** → retour à **Inactif**

### Règles qui travaillent ensemble
- Planifier un lavage la nuit.
- Synchroniser l’état (planifié / lavage / à vider).
- Notifier aux moments clés (démarrage prévu, cycle terminé, à vider).
- Réinitialiser l’état si un lavage est annulé.

Liens : [Commandes vocales](voice_commands.md)

---
Technical details: [Technical page](../technical/aspects/smart_dishwasher.md)
Détails techniques : [Page technique](../technical/aspects/smart_dishwasher.md)
