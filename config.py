import os

class Config:
    # Chiave segreta per Flask (necessaria per sessioni e form)
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersegreto')  # Sostituiscilo con una chiave più sicura

    # Configurazione MySQL con mysql-connector-python
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+mysqlconnector://root:admin@localhost/kodland'
    )

    # Disabilita le notifiche di modifica del database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
