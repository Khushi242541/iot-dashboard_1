
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Register routes/blueprints here
    from .routes import production_bp
    app.register_blueprint(production_bp)

    return app

 