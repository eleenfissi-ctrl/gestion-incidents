"""Tests des fonctionnalités principales : ajout, liste, détails, statut, suppression."""


def test_ajout_incident(client, incident_exemple):
    """Test 2 : l'ajout d'un incident fonctionne."""
    reponse = client.post("/incidents/nouveau", data=incident_exemple)
    assert reponse.status_code == 302  # redirection vers la liste = succès

    page = client.get("/").get_data(as_text=True)
    assert "Vidéoprojecteur en panne" in page


def test_liste_incidents(client, incident_exemple):
    """Test 3 : la liste des incidents est correctement retournée."""
    client.post("/incidents/nouveau", data=incident_exemple)
    client.post("/incidents/nouveau", data={**incident_exemple, "titre": "Wi-Fi coupé"})

    incidents = client.get("/api/incidents").get_json()
    assert len(incidents) == 2
    assert incidents[0]["titre"] == "Vidéoprojecteur en panne"
    assert incidents[0]["statut"] == "Nouveau"  # statut par défaut


def test_ajout_refuse_si_champ_vide(client, incident_exemple):
    reponse = client.post("/incidents/nouveau", data={**incident_exemple, "titre": ""})
    assert reponse.status_code == 400
    assert client.get("/api/incidents").get_json() == []


def test_details_incident(client, incident_exemple):
    client.post("/incidents/nouveau", data=incident_exemple)
    reponse = client.get("/incidents/1")
    assert reponse.status_code == 200
    assert "Salle B12" in reponse.get_data(as_text=True)


def test_details_incident_inexistant(client):
    assert client.get("/incidents/999").status_code == 404


def test_modifier_statut(client, incident_exemple):
    client.post("/incidents/nouveau", data=incident_exemple)
    client.post("/incidents/1/statut", data={"statut": "En cours"})
    assert client.get("/api/incidents").get_json()[0]["statut"] == "En cours"


def test_supprimer_incident(client, incident_exemple):
    client.post("/incidents/nouveau", data=incident_exemple)
    client.post("/incidents/1/supprimer")
    assert client.get("/api/incidents").get_json() == []
