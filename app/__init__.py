from flask import Flask, g, jsonify
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()


engine = create_engine(os.environ.get('DATABASE_URL'))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

jwt = JWTManager()

def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or {})
    
    jwt.init_app(app)

    @app.before_request
    def before_request():
        g.db = db_session
    
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    return app