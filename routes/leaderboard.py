from flask import Blueprint, render_template
from models import Utente

leaderboard_bp = Blueprint("leaderboard", __name__)

def get_top_users():
    """Restituisce la Top 10 degli utenti con il punteggio più alto."""
    return Utente.query.order_by(Utente.punteggio_totale.desc()).limit(10).all()
