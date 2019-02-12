from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

app = Flask(__name__)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

# Load configuration file
app.config.from_pyfile("config/defaults.py")
app.secret_key = app.config['SECRET_KEY']

from improvisor import routes, sockets