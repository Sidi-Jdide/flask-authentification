import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

class Config:
    # Clé secrète pour Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # URL de la base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Désactiver le suivi des modifications de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clé secrète pour JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')