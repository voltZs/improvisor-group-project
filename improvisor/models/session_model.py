from db import db
from datetime import datetime
from improvisor.models.associationTable_session_asset import session_asset
from flask_login import current_user

class SessionModel(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key = True)
    sessionName = db.Column(db.String(200))
    sessionNumber = db.Column(db.Integer)
    active = db.Column(db.Integer)
    dateCreated = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("UserModel")
    assets = db.relationship("AssetModel", secondary=session_asset, lazy="subquery", backref=db.backref("sessions", lazy=True))
    
    def json(self):
        return {"SessionName" : self.sessionName, "active" : self.active, "assets":[asset.assetname for asset in self.assets], "user_id" : self.user_id, "dateCreated" : self.dateCreated.__str__()}

    def __init__(self):
        num = next_session_num()
        self.sessionName = "Session " + str(num)
        self.sessionNumber = num
        self.user_id = current_user.get_id()
        self.active = 1
        self.dateCreated = datetime.now()
    
    def save_to_db(self):
        oldSession = SessionModel.query.filter_by(user_id = self.user_id,active = self.active).first()
        if(oldSession):
            oldSession.active = 0
        db.session.add(self)
        db.session.commit()
    
    def add_asset(self, assetObj, tab):
        self.assets.append(assetObj)
        assetObj.add_to_session(self.id, tab)

    @classmethod
    def find_by_sessionId(cls, id):
        return cls.query.filter_by(id=id, user_id=current_user.get_id()).first()

    @classmethod
    def find_by_sessionNumber(cls, number):
        return cls.query.filter_by(sessionNumber=number, user_id=current_user.get_id()).first()

def next_session_num():
    sessions = current_user.sessions
    max = 0
    if len(sessions) > 0:
        for session in sessions:
            if (max < session.sessionNumber):
                max = session.sessionNumber
    return max + 1