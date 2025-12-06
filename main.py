from flask import Flask
from config import Config
from supabase import create_client
import os

app = Flask(__name__)
app.config.from_object(Config)

# -------------------------------
# Supabase Init
# -------------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Make supabase available to blueprints
from app import auth, routes

# Register blueprints
app.register_blueprint(auth.auth_bp)
app.register_blueprint(routes.main_bp)

# Home route
@app.route("/")
def home():
    return "Hello Render"


if __name__ == "__main__":
    app.run(debug=True)
