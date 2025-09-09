from flask import Flask, jsonify, request
from mongoengine import connect
import os
from dotenv import load_dotenv

from entities.Persona.routes import persona_route
from matching import suggestions_module

load_dotenv()
app = Flask(__name__)

DB_URI = os.getenv("MONGO_URI")
connect(host=DB_URI)

@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Flask API!"})


app.register_blueprint(persona_route,url_prefix="/persona")
app.register_blueprint(suggestions_module, url_prefix="/suggestions")


if __name__ == '__main__':
    app.run(debug=True)


