from flask import Flask
from supabase import create_client, Client
from config import Config

supabase: Client = None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    global supabase
    if app.config['SUPABASE_URL'] and app.config['SUPABASE_KEY']:
        supabase = create_client(app.config['SUPABASE_URL'], app.config['SUPABASE_KEY'])
    else:
        print("Warning: Supabase URL or Key not set.")

    from app.auth import auth_bp
    from app.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
