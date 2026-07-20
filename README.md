# immo-alerts

Reçois chaque jour par email les nouvelles annonces d'appartements à
Versailles (78000), jusqu'à 200 000€, en tapant directement l'API JSON
publique de **Bien'ici** (pas de clé, pas de compte).

## Comment ça marche

1. Une **GitHub Action** se lance automatiquement chaque jour (cron dans
   `.github/workflows/daily.yml`).
2. Elle lit `config.yaml` (tes critères).
3. Elle interroge l'API de Bien'ici, filtre les annonces déjà vues
   (`seen.json`) et celles à exclure par mot-clé.
4. Elle t'envoie un email récapitulatif s'il y a du nouveau.

## Installation

### 1. Configure `config.yaml`

Déjà pré-rempli avec : Versailles 78000, appartements, achat, max 200 000€.
Modifie-le directement sur GitHub (bouton crayon ✏️) quand tu veux changer
tes critères — pas besoin de coder.

### 2. Configure l'envoi d'email

Si tu utilises Gmail :
- Active la validation en 2 étapes sur ton compte Google
- Crée un "mot de passe d'application" : https://myaccount.google.com/apppasswords

Dans les **Settings > Secrets and variables > Actions** de ton repo GitHub,
ajoute ces secrets :

| Secret       | Exemple (Gmail)              |
|--------------|-------------------------------|
| `SMTP_HOST`  | `smtp.gmail.com`              |
| `SMTP_PORT`  | `587`                          |
| `SMTP_USER`  | `toi@gmail.com`                |
| `SMTP_PASS`  | (le mot de passe d'application)|

### 3. Active les Actions

Onglet **Actions** de ton repo → active les workflows si demandé.
Tu peux lancer une exécution manuelle via "Run workflow" pour tester.

## Tester en local

```bash
pip install -r requirements.txt
export SMTP_HOST=smtp.gmail.com SMTP_PORT=587 SMTP_USER=toi@gmail.com SMTP_PASS=xxxx
python main.py
```

## Important à savoir

- **Source unique : Bien'ici.** C'est le seul portail qui offre une API
  JSON accessible sans blocage anti-bot. Ça ne couvre pas 100% du marché
  (SeLoger, Logic-immo, Leboncoin ne sont pas inclus — ils nécessitent des
  services payants type Apify pour contourner leurs protections).
- **Usage raisonnable** : ce script fait quelques requêtes par jour pour un
  usage personnel. C'est légal en France (collecte de données publiques
  accessibles, article L342-3 du code de la propriété intellectuelle),
  tant que l'extraction reste non-substantielle et sans revente. Ne
  transforme pas ça en usage commercial ou en extraction massive.
- **Fragilité** : l'API n'est pas officiellement documentée par Bien'ici.
  Si le site change sa structure, le script peut casser. Si ça arrive,
  dis-le moi et je l'adapte.
- Le fuseau horaire du cron GitHub Actions est UTC ; ajuste l'heure dans
  `daily.yml` si besoin (actuellement 07:00 UTC).
