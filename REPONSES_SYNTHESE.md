# Réponses aux questions de synthèse

> Aide à la révision : chaque étudiant doit pouvoir les expliquer avec ses propres mots.

**1. Différence entre Git et GitHub ?**
Git est un **outil** installé sur l'ordinateur qui enregistre l'historique des
modifications du code (commits, branches, fusions). GitHub est un **site web** qui
héberge des dépôts Git en ligne et ajoute la collaboration (Pull Requests, Actions,
Packages…). On peut utiliser Git sans GitHub, mais pas l'inverse.

**2. Rôle d'un Dockerfile ?**
C'est la **recette** pour construire une image Docker : image de base, fichiers à
copier, dépendances à installer, port, commande de démarrage. Tout le monde obtient
exactement la même image à partir de ce fichier.

**3. Différence entre une image et un conteneur ?**
L'**image** est un modèle figé, en lecture seule (comme une classe, ou un fichier
d'installation). Le **conteneur** est une image **en cours d'exécution** (comme un
objet, ou le programme lancé). Une même image peut lancer plusieurs conteneurs.

**4. Intérêt de Docker Compose ?**
Décrire dans **un seul fichier YAML** tout ce qu'il faut pour lancer l'application
(services, ports, volumes, redémarrage, variables) et tout démarrer ou arrêter avec
une seule commande (`docker compose up` / `down`), au lieu de longues commandes
`docker run`.

**5. Quel événement déclenche le workflow CI ?**
Un **push sur la branche `main`** et une **Pull Request vers `main`**
(section `on:` du fichier `ci.yml`).

**6. Pourquoi les tests doivent réussir avant la publication de l'image ?**
Pour ne **jamais publier une version cassée** : l'image publiée peut être déployée
directement. Dans `cd.yml`, `needs: tests` bloque la publication si un test échoue.

**7. Rôle de GHCR ?**
GitHub Container Registry est un **entrepôt d'images Docker** lié à GitHub. Il stocke
les images construites par le pipeline pour qu'on puisse les télécharger
(`docker pull`) depuis n'importe quelle machine.

**8. Pourquoi un tag correspondant au SHA du commit ?**
`latest` change à chaque publication, alors que le SHA est **unique et ne change
jamais**. On sait donc exactement quel code se trouve dans l'image (traçabilité) et on
peut **revenir à une version précédente** (rollback) en déployant un ancien SHA.

**9. Différence entre `docker build` et `docker pull` ?**
`docker build` **fabrique** une image localement à partir d'un Dockerfile et du code
source. `docker pull` **télécharge** une image déjà construite depuis un registre
(GHCR, Docker Hub). En déploiement, on fait un `pull` : pas besoin du code source.

**10. Étapes supplémentaires pour un déploiement automatique sur un serveur distant ?**
- Avoir un serveur (VM cloud) avec Docker installé.
- Stocker dans les **secrets GitHub** l'adresse du serveur et une clé SSH.
- Ajouter dans `cd.yml` un job `deploiement` (`needs: publication`) qui se connecte en
  SSH et exécute `docker compose -f compose.deploy.yaml pull && docker compose -f compose.deploy.yaml up -d`.
- Vérifier ensuite l'appli (ex. `curl http://serveur/health`) et prévoir un retour
  arrière (rollback) vers l'ancien tag SHA en cas d'échec.
- Optionnel : nom de domaine, HTTPS (reverse proxy Nginx/Traefik), supervision.
