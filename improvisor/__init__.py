import os
from db import db
from flask import Flask, session
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO


app = Flask(__name__)
CORS(app)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

# Load config file
app.config.from_pyfile("config/defaults.py")
# Setup server using config variables
app.secret_key = app.config['SECRET_KEY']

@app.before_first_request
def create_tables():
    db.create_all()

@app.before_first_request
def initialiseSession():
    session["user_id"] = 0
    session["logged_in"] = False
    session["selected_asset"] = ""


from improvisor import routes, sockets
