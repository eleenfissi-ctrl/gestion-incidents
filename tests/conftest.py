"""
Configuration commune des tests (pytest la charge automatiquement).

Chaque test reçoit une application neuve avec une base SQLite
temporaire : les tests ne touchent jamais à la vraie base.
"""
import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


@pytest.fixture
def incident_exemple():
    return {
        "titre": "Vidéoprojecteur en panne",
        "description": "Le vidéoprojecteur ne s'allume plus.",
        "lieu": "Salle B12",
        "priorite": "Élevée",
    }
