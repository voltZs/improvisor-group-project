
from flask_login import current_user
from flask_socketio import SocketIO, send, join_room, leave_room
from improvisor.models.asset_model import AssetModel
from improvisor.models.session_model import SessionModel
from improvisor import socketio
from datetime import datetime

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
    session = SessionModel.find_active_session()
    asset_id = data['id']
    #user_id = current_user.get_id()
    #date_added = datetime.now()
    tab = int(data['tab']) # not currently using, still needs to be added to date model

    asset = {}
    if id is not None:
        asset = AssetModel.find_by_assetId(asset_id).json()
        asset.pop('date-created')
    socketio.emit('presenter', asset, room=str(current_user.get_id()))

    asset = AssetModel.find_by_assetId(asset_id)
    session.assets.append(asset)
    asset.add_to_session(session.id)