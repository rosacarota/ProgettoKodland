from flask import Blueprint, jsonify, session, request, redirect, url_for
from models import db, Utente, Risposta, Compilazione
from quiz_logic import QuizGame
from routes.leaderboard import get_top_users

quiz_api_bp = Blueprint("quiz_api", __name__)

@quiz_api_bp.route("/api/get_questions", methods=["GET"])
def get_questions():
    """Restituisce tutte le domande e risposte del quiz selezionato in ordine casuale."""
    quiz_id = session.get("quiz_id")
    if not quiz_id:
        return jsonify({"error": "Quiz non avviato"}), 400

    game = QuizGame(quiz_id)
    return jsonify(game.get_all_questions())

@quiz_api_bp.route("/api/submit_quiz", methods=["POST"])
def submit_quiz():
    """Verifica le risposte e aggiorna il punteggio dell'utente nel database."""
    user_id = session.get("user_id")
    quiz_id = session.get("quiz_id")

    if not user_id or not quiz_id:
        return jsonify({"error": "Utente non loggato o quiz non avviato"}), 400

    data = request.get_json()
    answers = data.get("answers", {})

    correct_answers = 0
    for domanda_id, risposta_id in answers.items():
        correct = db.session.query(Risposta.giusta).filter_by(ID=risposta_id).scalar()
        if correct:
            correct_answers += 1

    # Controlla se l'utente ha già una compilazione per il quiz
    existing_compilation = Compilazione.query.filter_by(utente=user_id, quiz=quiz_id).first()

    if existing_compilation:
        existing_compilation.punteggio = correct_answers  # Aggiorna il punteggio esistente
    else:
        new_compilation = Compilazione(utente=user_id, quiz=quiz_id, punteggio=correct_answers)
        db.session.add(new_compilation)

    # Aggiorna il punteggio totale dell'utente
    user = Utente.query.get(user_id)
    if user:
        user.punteggio_totale += correct_answers

    db.session.commit()

    # Salva il punteggio nella sessione per mostrarlo nella pagina di congratulazioni
    session["last_quiz_score"] = correct_answers
    session["total_score"] = user.punteggio_totale

    return jsonify({"redirect": url_for("quiz_api.congratulations")})  # Restituisce il link per il redirect

@quiz_api_bp.route("/quiz/congratulations")
def congratulations():
    """Mostra la pagina di congratulazioni dopo il quiz."""
    last_quiz_score = session.pop("last_quiz_score", 0)
    total_score = session.pop("total_score", 0)
    return redirect(url_for("quiz.show_congratulations", quiz_score=last_quiz_score, total_score=total_score))
