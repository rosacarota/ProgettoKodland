from flask import Blueprint, render_template
from routes.leaderboard import get_top_users  # Importiamo la funzione

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    """Homepage con la classifica Top 10 sotto."""
    top_users = get_top_users()  # Otteniamo la Top 10
    return render_template("index.html", top_users=top_users)
