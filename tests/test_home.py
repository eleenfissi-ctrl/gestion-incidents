"""Test 1 : la page d'accueil est accessible."""


def test_page_accueil_accessible(client):
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert "Liste des incidents" in reponse.get_data(as_text=True)


def test_route_sante(client):
    reponse = client.get("/health")
    assert reponse.status_code == 200
    assert reponse.get_json() == {"status": "ok"}
