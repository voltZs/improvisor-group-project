
from flask_login import current_user
from flask_socketio import SocketIO, send, join_room, leave_room
from improvisor.models.asset_model import AssetModel
from improvisor import socketio

@socketio.on('join')
def on_join():
    room = str(current_user.get_id())
    join_room(room)


@socketio.on('leave')
def on_leave():
    room = str(current_user.get_id())
    leave_room(room)


@socketio.on('event')
def handleMessage(data):
    id = data
    asset = {}
    if id is not None:
        asset = AssetModel.find_by_assetId(id).json()
        asset.pop('date-created')
    socketio.emit('presenter', asset, room=str(current_user.get_id()))