from db import db
from improvisor.models.associationTable_tag_asset import asset_tags
from flask import session

class AssetModel(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    assetname = db.Column(db.String(200))
    assetLocation = db.Column(db.String(200), nullable = True)
    thumbnailLocation = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    user = db.relationship("UserModel")
    tags = db.relationship("TagModel",secondary=asset_tags, lazy="subquery", backref=db.backref("assets", lazy=True))

    def json(self):
        return {"asset": self.assetname, "tags" : [tag.json() for tag in self.tags],"user": self.user_id, "assetLocation" : self.assetLocation, "thumbnailLocation" : self.thumbnailLocation}

    def __init__(self, assetname, user_id, assetLocation = None, thumbnailLocation = None):
        self.assetname = assetname 
        self.user_id = user_id
        self.assetLocation = assetLocation
        self.thumbnailLocation = thumbnailLocation
        
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_assetName(cls, assetname):
        return cls.query.filter_by(assetname = assetname, user_id = session["user_id"]).first()