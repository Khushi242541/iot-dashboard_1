#Our server initializer 
from flask import Flask
from backend.server.routes import Production
from backend.server.mongo import *
from backend.server.__init__ import *
from frontend.gui_ import launch_gui

if __name__ == "__main__":
    launch_gui()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(Production)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
 