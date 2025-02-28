import random
from flask import session
from models import db, Domanda, Risposta, Composizione_Domanda, Composizione_Quiz

class QuizGame:
    def __init__(self, quiz_id):
        self.quiz_id = quiz_id
        self.questions = self.load_questions()

    def load_questions(self):
        """Carica tutte le domande associate al quiz e ottiene le risposte tramite Composizione_Domanda."""
        domande = db.session.query(Domanda).join(Composizione_Quiz).filter(
            Composizione_Quiz.quiz == self.quiz_id
        ).all()

        questions_data = []
        for domanda in domande:
            risposte = db.session.query(Risposta).join(Composizione_Domanda).filter(
                Composizione_Domanda.domanda == domanda.ID
            ).all()
            random.shuffle(risposte)  # Mescola le risposte

            questions_data.append({
                "id": domanda.ID,
                "testo": domanda.testo,
                "risposte": [{"id": r.ID, "testo": r.testo, "giusta": r.giusta} for r in risposte]
            })

        random.shuffle(questions_data)  # Mescola l'ordine delle domande
        return questions_data

    def get_all_questions(self):
        """Restituisce tutte le domande e risposte in ordine casuale."""
        return self.questions
