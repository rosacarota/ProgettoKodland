from flask import Blueprint, render_template, request, redirect, url_for, jsonify  # ⬅️ Aggiunto redirect e url_for
from models import db, Utente
from werkzeug.security import generate_password_hash


registrazione_bp = Blueprint("registrazione", __name__)

@registrazione_bp.route("/registrazione", methods=["GET", "POST"])
def registrazione():
    if request.method == "POST":
        nickname = request.form["nickname"]
        email = request.form["email"]
        password = request.form["password"]

        # Cripta la password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Crea un nuovo utente
        nuovo_utente = Utente(nickname=nickname, email=email, password=hashed_password)

        db.session.add(nuovo_utente)
        db.session.commit()  # Salva nel database

        return redirect(url_for("login.login"))  # Dopo la registrazione, reindirizza al login

    return render_template("registrazione.html")

# **Nuova route per il controllo AJAX**
@registrazione_bp.route("/check_nickname_email", methods=["POST"])
def check_nickname_email():
    data = request.get_json()
    nickname = data.get("nickname")
    email = data.get("email")

    nickname_esistente = Utente.query.filter_by(nickname=nickname).first() is not None
    email_esistente = Utente.query.filter_by(email=email).first() is not None

    return jsonify({"nickname_esistente": nickname_esistente, "email_esistente": email_esistente})
