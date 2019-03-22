
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
    #print(session.active)
    fromTabs = data['fromTabs']
    asset_id = data['id']
    tab = int(data['tab'])
    print("ID: " + asset_id + " Tab: " + str(tab))
    asset = {}
    if asset_id is not None:
        asset = AssetModel.find_by_assetId(asset_id).json()
        asset.pop('date-created')
        socketio.emit('presenter', asset, room=str(current_user.get_id()))
    
    if (not fromTabs):
        asset = AssetModel.find_by_assetId(asset_id)
        if (session):
            session.add_asset(asset, tab)
        else:
            print("No active session")