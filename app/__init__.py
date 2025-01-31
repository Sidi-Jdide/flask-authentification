from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

# Initialiser SQLAlchemy
engine = create_engine(os.environ.get('DATABASE_URL'))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Initialiser JWT
jwt = JWTManager()

def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or {})
    
    # Configurer JWT
    jwt.init_app(app)

    # Stocker la session de la base de données dans g avant chaque requête
    @app.before_request
    def before_request():
        g.db = db_session

    # Fermer la session de la base de données après chaque requête
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Importer et enregistrer les routes
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    # Créer les tables de la base de données
    with app.app_context():
        Base.metadata.create_all(bind=engine)

    return app