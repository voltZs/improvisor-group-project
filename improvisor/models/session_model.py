from db import db
from datetime import datetime
from improvisor.models.associationTable_session_asset import session_asset
from flask_login import current_user

class SessionModel(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key = True)
    active = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("UserModel")
    assets = db.relationship("AssetModel", secondary=session_asset, lazy="subquery", backref=db.backref("sessions", lazy=True))
    
    def json(self):
        return {"active" : self.active, "assets":[asset.assetname for asset in self.assets], "user_id" : self.user_id}

    def __init__(self, user_id, active=1 ):
        self.user_id = user_id
        self.active = active
        
    
    def save_to_db(self):
        oldSession = SessionModel.query.filter_by(user_id = self.user_id,active = self.active).first()
        if(oldSession):
            oldSession.active = 0
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_sessionId(cls, id):
        return cls.query.filter_by(id=id, user_id=current_user.get_id()).first()