from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from server.routes import Production  # Import the Blueprint

app = Flask(__name__)
app.register_blueprint(Production)
CORS(app)  #To enable CORS globally

# Example route to verify it's running
@app.route("/")
def home():
    return jsonify({"message": "Server is running successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
