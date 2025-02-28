from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabella Utente
class Utente(db.Model):
    __tablename__ = "Utente"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    punteggio_totale = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Tabella Quiz
class Quiz(db.Model):
    __tablename__ = "Quiz"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titolo = db.Column(db.String(50), nullable=False)
    argomento = db.Column(db.String(50), nullable=False)

# Tabella Domanda
class Domanda(db.Model):
    __tablename__ = "Domanda"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    testo = db.Column(db.String(500), nullable=False)

# Tabella Risposta
class Risposta(db.Model):
    __tablename__ = "Risposta"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    testo = db.Column(db.String(500), nullable=False)
    giusta = db.Column(db.Boolean, nullable=False)  # Indica se la risposta è corretta

# Tabella Compilazione (Associazione Utente-Quiz con punteggio)
class Compilazione(db.Model):
    __tablename__ = "Compilazione"
    utente = db.Column(db.Integer, db.ForeignKey("Utente.ID"), primary_key=True)
    quiz = db.Column(db.Integer, db.ForeignKey("Quiz.ID"), primary_key=True)
    punteggio = db.Column(db.Integer, default=0)

# Tabella Composizione_Quiz (Associazione Quiz-Domande)
class Composizione_Quiz(db.Model):
    __tablename__ = "Composizione_Quiz"
    quiz = db.Column(db.Integer, db.ForeignKey("Quiz.ID"), primary_key=True)
    domanda = db.Column(db.Integer, db.ForeignKey("Domanda.ID"), primary_key=True)

# Tabella Composizione_Domanda (Associazione Domanda-Risposte)
class Composizione_Domanda(db.Model):
    __tablename__ = "Composizione_Domanda"
    domanda = db.Column(db.Integer, db.ForeignKey("Domanda.ID"), primary_key=True)
    risposta = db.Column(db.Integer, db.ForeignKey("Risposta.ID"), primary_key=True)
