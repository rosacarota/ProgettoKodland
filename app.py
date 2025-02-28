import webbrowser
from flask import Flask
from requests import Session
from models import db
from routes.leaderboard import leaderboard_bp
from routes.login import login_bp
from routes.quiz_api import quiz_api_bp
from routes.registrazione import registrazione_bp
from routes.home import home_bp
from routes.quiz import quiz_bp
from utils import login_required

app = Flask(__name__)
app.config.from_object('config.Config')

# Inizializza il database
db.init_app(app)
Session()

# Registra i blueprint
app.register_blueprint(registrazione_bp) # Registrazione
app.register_blueprint(home_bp)          # Home
app.register_blueprint(login_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(quiz_api_bp)
app.register_blueprint(leaderboard_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea le tabelle nel database se non esistono
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
