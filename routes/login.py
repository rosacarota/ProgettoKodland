from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Utente
from werkzeug.security import check_password_hash
from flask import session

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Cerca l'utente nel database
        utente = Utente.query.filter_by(email=email).first()

        # Controlla se l'utente esiste e la password è corretta
        if utente and check_password_hash(utente.password, password):
            session["user_id"] = utente.ID  # Salva l'ID dell'utente nella sessione
            session["nickname"] = utente.nickname
            return redirect(url_for("home.home"))  # Reindirizza alla home

        return render_template("login.html", error="Credenziali errate. Riprova.")

    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.clear()  # Cancella tutti i dati della sessione
    return redirect(url_for("home.home"))  # Reindirizza alla homepage

