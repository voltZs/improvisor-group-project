from db import db  
from datetime import datetime
from flask_login import current_user

class DateModel(db.Model):
    __tablename__ = "dates"

    id = db.Column(db.Integer, primary_key = True)
    dateAdded = db.Column(db.DateTime)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"))
    session_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    tab = db.Column(db.Integer)

    asset = db.relationship("AssetModel")

    def json(self):
        return {"session_id":self.session_id, "asset" : self.asset.json(), "asset_id" : self.asset_id, "dateAdded" : self.dateAdded.__str__(), "tab" : self.tab}

    def __init__(self, asset_id, session_id, user_id, tab):
        self.asset_id = asset_id
        self.session_id = session_id
        self.user_id =  user_id
        self.dateAdded = datetime.now()
        self.tab = tab

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_sessionNum(cls, id):
        return cls.query.filter_by(session_id=id, user_id=current_user.get_id())