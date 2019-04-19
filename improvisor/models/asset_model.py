from db import db
from improvisor.models.associationTable_tag_asset import asset_tags
from improvisor.models.date_model import DateModel
from flask import session
from datetime import datetime
from flask_login import current_user
from improvisor.models.session_model import SessionModel
import os

class AssetModel(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    assettype = db.Column(db.String(10))
    assetname = db.Column(db.String(200))
    assetLocation = db.Column(db.String(200), nullable = True)
    assetLink = db.Column(db.String(200), nullable = True)
    thumbnailLocation = db.Column(db.String(200), nullable=True)
    dateCreated = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))



    user = db.relationship("UserModel")
    # sessionDates = db.relationship("DateModel", primaryjoin= "and_(AssetModel.id==DateModel.asset_id, "
    #                                             "AssetModel.user.activeSession.id == DateModel.session_id) ")
    tags = db.relationship("TagModel",secondary=asset_tags, lazy="subquery", backref=db.backref("assets", lazy=True))
    sessionDates = db.relationship("DateModel", lazy = "dynamic")
    def json(self):
        return {"id": self.id, "assetname": self.assetname, "assettype": self.assettype, "tags" : [tag.tagname for tag in self.tags],"user": self.user_id, "assetLocation" : self.assetLocation, "assetLink": self.assetLink, "thumbnailLocation" : self.thumbnailLocation, "date-created" : self.dateCreated.__str__(), "sessions": [session.id for session in self.sessions]}

    def __init__(self, assetname, user_id, assettype, assetLocation = None, assetLink = None, thumbnailLocation = None, dateCreated = datetime.now()):
        self.assetname = assetname
        self.assettype = assettype
        self.user_id = user_id
        self.assetLocation = assetLocation
        self.assetLink = assetLink
        self.thumbnailLocation = thumbnailLocation
        self.dateCreated = dateCreated


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def add_to_session(self, session_id, tab):
        date = DateModel(self.id, session_id, self.user_id, tab)
        self.sessionDates.append(date)
        db.session.commit()

    def get_dates_for_session(self, sessionNumber):
        actual_session_id = SessionModel.find_by_sessionNumber(sessionNumber)
        datesForSession = [date for date in self.sessionDates if date.session_id == actual_session_id.id]
        return datesForSession

    def get_user_session_appearances(self):
        return [session for session in self.sessions if session.user_id == self.user_id]

    @classmethod
    def find_by_assetName(cls, assetname):
        return cls.query.filter_by(assetname = assetname, user_id = session["user_id"]).all()

    @classmethod
    def find_by_assetId(cls, id):
        return cls.query.filter_by(id=id, user_id=current_user.get_id()).first()

    @classmethod
    def delete_by_assetId(cls, id):
        obj = cls.query.filter_by(id=id, user_id=current_user.get_id()).first()
        directories = obj.thumbnailLocation.split("/")
        del directories[0]
        directories.insert(0, "improvisor")
        path = "/".join([directory for directory in directories if "Thumbnail" not in directory])
        if obj.assettype == "file":
            os.remove("improvisor" + obj.assetLocation)
        os.remove("improvisor" + obj.thumbnailLocation)
        os.rmdir(path)
        db.session.delete(obj)
        db.session.commit()
