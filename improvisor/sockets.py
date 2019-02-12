from flask_socketio import SocketIO, send
from improvisor import socketio

@socketio.on('event')
def handleMessage(data):
    print('Event: ' + str(data))
    filename = str(data) + ".jpg"
    socketio.emit('presenter', filename)