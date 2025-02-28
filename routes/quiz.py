from flask import Blueprint, render_template, session, redirect, url_for

from routes.leaderboard import get_top_users
from utils import login_required
from models import db, Quiz
from quiz_logic import QuizGame  # ⬅️ Modifica QUI, sostituisci QuizSession con QuizGame

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/quiz")
@login_required
def quiz_list():
    """Mostra la lista dei quiz disponibili."""
    quiz = Quiz.query.all()
    return render_template("quiz_list.html", quiz=quiz)

@quiz_bp.route("/quiz/<int:quiz_id>")
@login_required
def start_quiz(quiz_id):
    """Inizializza il quiz selezionato."""
    session["quiz_id"] = quiz_id  # Salva l'ID del quiz nella sessione
    QuizGame(quiz_id).load_questions()  # Carica le domande e le mescola
    return redirect(url_for("quiz.quiz_page"))

@quiz_bp.route("/quiz/play")
@login_required
def quiz_page():
    """Mostra la pagina del quiz con il carosello di domande."""
    return render_template("quiz.html")

@quiz_bp.route("/quiz/congratulations/<int:quiz_score>/<int:total_score>")
@login_required
def show_congratulations(quiz_score, total_score):
    top_users = get_top_users()
    """Mostra la pagina di congratulazioni con i punteggi."""
    return render_template("quiz_congratulations.html", quiz_score=quiz_score, total_score=total_score, top_users=top_users)