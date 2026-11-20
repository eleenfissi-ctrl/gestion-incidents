"""
Point d'entrée de l'application Flask.

La fonction create_app() fabrique l'application. On l'utilise :
  - pour lancer le site (gunicorn "app:create_app()")
  - dans les tests (avec une base de données temporaire)
"""
import os

from flask import Flask

from . import db
from .routes import bp


def create_app(config=None):
    app = Flask(__name__)

    # Chemin de la base SQLite. Dans Docker, on le change avec la
    # variable d'environnement DATABASE (ex : /data/incidents.db).
    app.config["DATABASE"] = os.environ.get(
        "DATABASE", os.path.join(app.root_path, "..", "incidents.db")
    )

    # Les tests peuvent remplacer la configuration.
    if config:
        app.config.update(config)

    db.init_app(app)
    app.register_blueprint(bp)

    # Route de santé : permet de vérifier rapidement que l'appli tourne.
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
