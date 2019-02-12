from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

app = Flask(__name__)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

# Load config file
app.config.from_pyfile("config/defaults.py")
# Setup server using config variables
app.secret_key = app.config['SECRET_KEY']

from improvisor import routes, sockets