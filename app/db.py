"""
Gestion de la base de données SQLite.

SQLite stocke toute la base dans un seul fichier : pas de serveur
de base de données à installer.
"""
import os
import sqlite3

from flask import current_app, g

# Valeurs autorisées (utilisées aussi dans les formulaires).
PRIORITES = ["Faible", "Moyenne", "Élevée"]
STATUTS = ["Nouveau", "En cours", "Résolu"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS incidents (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identifiant unique
    titre       TEXT NOT NULL,
    description TEXT NOT NULL,
    lieu        TEXT NOT NULL,                      -- Salle ou laboratoire
    priorite    TEXT NOT NULL,                      -- Faible / Moyenne / Élevée
    statut      TEXT NOT NULL DEFAULT 'Nouveau'     -- Nouveau / En cours / Résolu
);
"""


def get_db():
    """Ouvre (une seule fois par requête) une connexion à la base."""
    if "db" not in g:
        chemin = current_app.config["DATABASE"]
        dossier = os.path.dirname(os.path.abspath(chemin))
        os.makedirs(dossier, exist_ok=True)
        g.db = sqlite3.connect(chemin)
        g.db.row_factory = sqlite3.Row  # accès aux colonnes par leur nom
    return g.db


def close_db(e=None):
    """Ferme la connexion à la fin de chaque requête."""
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_db():
    """Crée la table si elle n'existe pas encore."""
    get_db().executescript(SCHEMA)


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
