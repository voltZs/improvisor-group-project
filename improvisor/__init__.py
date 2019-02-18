import os
from db import db
from flask import Flask, session
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'yeet'

@app.before_first_request
def create_tables():
    db.create_all()

@app.before_first_request
def initialiseSession():
    session["user_id"] = 0
    session["logged_in"] = False





from improvisor import routes