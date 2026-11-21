# 🛠️ Gestion des incidents informatiques — Mini-projet DevOps 2026

Application web qui permet aux étudiants et enseignants de **signaler des incidents
informatiques** (panne de PC, vidéoprojecteur, Wi-Fi…) et de **suivre leur traitement**.

Le projet met en place une chaîne DevOps complète :

```
Code  →  Git/GitHub  →  GitHub Actions (tests)  →  Image Docker  →  GHCR  →  Déploiement Compose
```

---

## 📌 Sommaire

1. [L'idée en 1 minute](#-lidée-en-1-minute)
2. [Technologies](#-technologies)
3. [Structure du projet](#-structure-du-projet)
4. [Mission 1 — Lancer l'application en local](#mission-1--lapplication-web)
5. [Mission 2 — Git et GitHub](#mission-2--git-et-github)
6. [Mission 3 — Docker](#mission-3--docker)
7. [Mission 4 — Docker Compose](#mission-4--docker-compose)
8. [Mission 5 — Intégration continue (CI)](#mission-5--intégration-continue-ci)
9. [Mission 6 — Publication dans GHCR (CD)](#mission-6--publication-dans-ghcr-cd)
10. [Mission 7 — Déploiement](#mission-7--déploiement)
11. [Captures d'écran à fournir](#-captures-décran-à-fournir)

---

## 💡 L'idée en 1 minute

| Étape | Outil | En une phrase |
|---|---|---|
| Écrire l'application | **Flask + SQLite** | Un petit site Python qui enregistre les incidents dans un fichier de base de données. |
| Sauvegarder le code | **Git / GitHub** | Git garde l'historique des modifications, GitHub l'héberge en ligne. |
| Empaqueter | **Docker** | On met l'appli + Python + dépendances dans une « boîte » (image) qui marche partout. |
| Lancer facilement | **Docker Compose** | Un fichier qui décrit comment lancer le conteneur (port, volume…) : une seule commande. |
| Vérifier automatiquement | **GitHub Actions (CI)** | À chaque push, GitHub lance les tests et construit l'image. |
| Publier | **GHCR (CD)** | Si les tests passent, l'image est envoyée dans le registre de GitHub. |
| Déployer | **compose.deploy.yaml** | Un serveur télécharge l'image depuis GHCR et la lance, sans rien recompiler. |

---

## 🧰 Technologies

- Python 3.12, **Flask** (framework web), **SQLite** (base de données dans un fichier)
- **pytest** (tests automatisés), **gunicorn** (serveur web de production)
- Docker, Docker Compose, GitHub Actions, GitHub Container Registry

---

## 📁 Structure du projet

```
gestion-incidents/
├── app/                        # L'application Flask
│   ├── __init__.py             #   crée l'application (create_app)
│   ├── db.py                   #   base SQLite : table "incidents"
│   ├── routes.py               #   les pages : ajouter, lister, détails, statut, supprimer
│   ├── templates/              #   les pages HTML
│   └── static/style.css        #   le style
├── tests/
│   ├── conftest.py             # préparation des tests (base temporaire)
│   ├── test_home.py            # la page d'accueil répond
│   └── test_incidents.py       # ajout, liste, détails, statut, suppression
├── Dockerfile                  # recette de l'image Docker
├── compose.yaml                # lancement en développement (construit l'image)
├── compose.deploy.yaml         # lancement en production (image GHCR)
├── requirements.txt            # dépendances Python
├── .gitignore / .dockerignore
└── .github/workflows/
    ├── ci.yml                  # tests + vérif compose + build
    └── cd.yml                  # tests puis publication dans GHCR
```

### Un incident contient

| Champ | Exemple |
|---|---|
| Identifiant | 1 (automatique) |
| Titre | Vidéoprojecteur en panne |
| Description | Il ne s'allume plus |
| Lieu | Salle B12 |
| Priorité | Faible / Moyenne / Élevée |
| Statut | Nouveau / En cours / Résolu (« Nouveau » à la création) |

---

## Mission 1 — L'application web

### Lancer en local (sans Docker)

```bash
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt
flask --app app run --debug
```

Ouvrir **http://localhost:5000**

### Les 5 fonctionnalités

| Fonctionnalité | Où ? |
|---|---|
| 1. Ajouter un incident | bouton **+ Nouvel incident** |
| 2. Afficher la liste | page d'accueil `/` |
| 3. Consulter les détails | lien **Détails** dans la liste |
| 4. Modifier le statut | liste déroulante sur la page détails |
| 5. Supprimer | bouton rouge **Supprimer** sur la page détails |

Bonus : `/api/incidents` renvoie la liste en JSON et `/health` indique si l'appli tourne.

### Lancer les tests

```bash
pytest -v
```
→ 9 tests doivent passer ✅

---

## Mission 2 — Git et GitHub

```bash
# 1. Initialiser le dépôt
git init
git branch -M main

# 2-4. Premiers commits (messages explicites !)
git add .gitignore README.md
git commit -m "Initialisation du projet : README et .gitignore"
git add app/ requirements.txt
git commit -m "Ajout de l'application Flask de gestion des incidents"
git add tests/
git commit -m "Ajout des tests automatisés"

# 5. Créer la branche demandée
git checkout -b feature/gestion-incidents

# 6. Faire une modification dans cette branche, puis :
git add .
git commit -m "Ajout de la suppression d'un incident"

# 7. Revenir sur main et fusionner
git checkout main
git merge feature/gestion-incidents

# 8. Envoyer sur GitHub (créer d'abord un dépôt vide "gestion-incidents" sur github.com)
git remote add origin https://github.com/eleenfissi-ctrl/gestion-incidents.git
git push -u origin main
git push origin feature/gestion-incidents
```

Vérifier l'historique : `git log --oneline --graph --all`

---

## Mission 3 — Docker

Le `Dockerfile` contient les 6 éléments demandés : image de base (`FROM`), répertoire
de travail (`WORKDIR`), copie des fichiers (`COPY`), installation des dépendances
(`RUN pip install`), port (`EXPOSE 5000`) et commande de démarrage (`CMD`).

```bash
# 1. Construire l'image
docker build -t gestion-incidents .

# 2. Lancer un conteneur
docker run -d -p 5000:5000 --name incidents gestion-incidents

# 3. Vérifier le conteneur
docker ps
docker logs incidents

# 4. Tester : ouvrir http://localhost:5000

# Arrêter et supprimer
docker stop incidents && docker rm incidents
```

---

## Mission 4 — Docker Compose

`compose.yaml` définit : le service `web`, la construction (`build: .`), le port `5000`,
la politique `restart: unless-stopped` et un **volume** `incidents-data` pour garder
la base de données même si on supprime le conteneur.

```bash
docker compose up -d --build     # 1. Démarrer
docker compose ps                # 2. Vérifier les services
docker compose logs -f           # 3. Consulter les journaux (Ctrl+C pour quitter)
docker compose down              # 4. Arrêter
```

---

## Mission 5 — Intégration continue (CI)

Fichier : `.github/workflows/ci.yml`

**Quand ?** À chaque `push` sur `main` et à chaque Pull Request vers `main`.

**Quoi ?**
1. Récupère le code (`actions/checkout`)
2. Installe Python 3.12 et les dépendances
3. Lance `pytest`
4. Vérifie `compose.yaml` (`docker compose config`)
5. Construit l'image (`docker build`)

Résultat visible dans l'onglet **Actions** du dépôt GitHub.

### Expérience obligatoire : provoquer une erreur

1. Dans `app/routes.py`, remplacer temporairement `'Nouveau'` par `'Ouvert'` dans la requête `INSERT`.
2. `git commit -am "Test : erreur volontaire" && git push`
3. Onglet **Actions** → le pipeline est **rouge ❌** ; l'étape **Lancer les tests** a échoué
   (`test_liste_incidents` attend le statut « Nouveau »). 📸 *Capture*
4. Remettre `'Nouveau'`.
5. `git commit -am "Correction de l'erreur volontaire" && git push`
6. Le pipeline redevient **vert ✅**. 📸 *Capture*

---

## Mission 6 — Publication dans GHCR (CD)

Fichier : `.github/workflows/cd.yml` — déclenché à chaque push sur `main`.

- **Job `tests`** : lance pytest.
- **Job `publication`** : `needs: tests` → il ne démarre **que si les tests réussissent**.
  - permission `packages: write`
  - connexion à `ghcr.io` avec `GITHUB_TOKEN` (fourni automatiquement, aucun secret à créer)
  - publie l'image avec **2 tags** : `latest` et le SHA du commit

### Vérifier

Sur GitHub : page du profil → onglet **Packages** → `gestion-incidents` → voir les tags. 📸 *Capture*

> 💡 Pour que tout le monde puisse télécharger l'image sans se connecter :
> Package → **Package settings** → **Change visibility** → *Public*.

Sur le terminal :
```bash
docker pull ghcr.io/nom-utilisateur/gestion-incidents:latest
docker images
```

> Si le package est privé, il faut d'abord se connecter :
> `docker login ghcr.io -u NOM-UTILISATEUR` (mot de passe = un *Personal Access Token*
> avec le droit `read:packages`). **Ne partagez jamais ce jeton.**

---

## Mission 7 — Déploiement

`compose.deploy.yaml` utilise **directement l'image de GHCR** (pas de `build`).
⚠️ Remplacer `nom-utilisateur` par votre nom GitHub **en minuscules**.

```bash
docker compose -f compose.deploy.yaml pull       # 1. Récupérer l'image
docker compose -f compose.deploy.yaml up -d      # 2. Démarrer
docker compose -f compose.deploy.yaml ps         # 3. Vérifier
docker compose -f compose.deploy.yaml logs       # 4. Journaux
```

Ouvrir **http://localhost:8080** et tester ajout / liste / détails / statut / suppression. 📸 *Capture*

### Mettre à jour l'application

1. Modifier quelque chose (ex. le titre dans `app/templates/base.html`).
2. `git commit -am "Modification du titre de l'application" && git push`
3. Vérifier que CI et CD sont verts dans **Actions**.
4. Vérifier le nouveau tag (SHA) dans **Packages**.
5. Sur la machine de déploiement :
   ```bash
   docker compose -f compose.deploy.yaml pull
   docker compose -f compose.deploy.yaml up -d
   ```
6. Rafraîchir le navigateur : la nouvelle version est en ligne ✅
   (les incidents sont conservés grâce au volume).

---

## 📸 Captures d'écran à fournir

À placer dans un dossier `captures/` du dépôt :

| N° | Capture |
|---|---|
| 1 | Pipeline CI réussi (onglet Actions, vert) |
| 2 | Pipeline en échec avec l'étape « Lancer les tests » en rouge |
| 3 | Pipeline corrigé (vert) |
| 4 | Package GHCR avec les tags `latest` et SHA |
| 5 | `docker pull` + `docker images` dans le terminal |
| 6 | Application déployée dans le navigateur (port 8080) |
| 7 | Nouvelle version après mise à jour |

---

## 👥 Auteurs

- Étudiant 1 — *nfissi alaa*
- Étudiant 2 — *daghfous ines*

DSI3 — Module DevOps 2026-2027
