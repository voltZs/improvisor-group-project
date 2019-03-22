import os
from db import db
from flask import Flask, session
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.debug = True

# Load config file
app.config.from_pyfile("config/defaults.py")
# Setup server using config variables
app.secret_key = app.config['SECRET_KEY']

# Connect to the mail server
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

CORS(app)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)
db.init_app(app)


@app.before_first_request
def initialisation():
    db.create_all()
    session["selected_asset"] = ""
    if not os.path.exists("improvisor/static/resources/uploadedFiles"):
        os.mkdir("improvisor/static/resources/uploadedFiles")

from improvisor import routes, sockets
