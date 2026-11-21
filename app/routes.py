"""
Les pages de l'application (les « routes »).

  GET  /                          -> liste des incidents
  GET  /incidents/nouveau         -> formulaire d'ajout
  POST /incidents/nouveau         -> enregistre un incident
  GET  /incidents/<id>            -> détails d'un incident
  POST /incidents/<id>/statut     -> modifie le statut
  POST /incidents/<id>/supprimer  -> supprime l'incident
  GET  /api/incidents             -> liste au format JSON (utile pour les tests)
"""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from .db import PRIORITES, STATUTS, get_db

bp = Blueprint("incidents", __name__)


def trouver_incident(incident_id):
    incident = get_db().execute(
        "SELECT * FROM incidents WHERE id = ?", (incident_id,)
    ).fetchone()
    if incident is None:
        abort(404)
    return incident


# 2. Afficher la liste des incidents
@bp.get("/")
def liste():
    incidents = get_db().execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()
    return render_template("liste.html", incidents=incidents)


# 1. Ajouter un incident
@bp.route("/incidents/nouveau", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        titre = request.form.get("titre", "").strip()
        description = request.form.get("description", "").strip()
        lieu = request.form.get("lieu", "").strip()
        priorite = request.form.get("priorite", "")

        # Vérification simple des champs
        if not titre or not description or not lieu or priorite not in PRIORITES:
            return render_template(
                "formulaire.html", priorites=PRIORITES,
                erreur="Tous les champs sont obligatoires.", form=request.form,
            ), 400

        db = get_db()
        db.execute(
            "INSERT INTO incidents (titre, description, lieu, priorite, statut) "
            "VALUES (?, ?, ?, ?, 'Ouvert')",
            (titre, description, lieu, priorite),
        )
        db.commit()
        return redirect(url_for("incidents.liste"))

    return render_template("formulaire.html", priorites=PRIORITES, form={})


# 3. Consulter les détails d'un incident
@bp.get("/incidents/<int:incident_id>")
def details(incident_id):
    return render_template(
        "details.html", incident=trouver_incident(incident_id), statuts=STATUTS
    )


# 4. Modifier le statut d'un incident
@bp.post("/incidents/<int:incident_id>/statut")
def modifier_statut(incident_id):
    trouver_incident(incident_id)
    statut = request.form.get("statut", "")
    if statut not in STATUTS:
        abort(400)
    db = get_db()
    db.execute("UPDATE incidents SET statut = ? WHERE id = ?", (statut, incident_id))
    db.commit()
    return redirect(url_for("incidents.details", incident_id=incident_id))


# 5. Supprimer un incident
@bp.post("/incidents/<int:incident_id>/supprimer")
def supprimer(incident_id):
    trouver_incident(incident_id)
    db = get_db()
    db.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
    db.commit()
    return redirect(url_for("incidents.liste"))


# Bonus : la liste au format JSON
@bp.get("/api/incidents")
def api_liste():
    lignes = get_db().execute("SELECT * FROM incidents ORDER BY id").fetchall()
    return [dict(ligne) for ligne in lignes]
