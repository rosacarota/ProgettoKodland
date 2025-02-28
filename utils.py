from flask import session, redirect, url_for
from functools import wraps  # Necessario per creare decoratori

def login_required(f):
    @wraps(f)  # Mantiene il nome e la docstring della funzione originale
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:  # Se l'utente non è loggato
            return redirect(url_for("login.login"))  # Reindirizza al login
        return f(*args, **kwargs)  # Altrimenti esegue la funzione normalmente
    return decorated_function
