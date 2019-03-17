from db import db
from flask_login import UserMixin
from sqlalchemy import func

class UserModel(UserMixin, db.Model):
    defaultImage = "https://media.istockphoto.com/photos/portrait-of-a-businessman-picture-id619636712?k=6&m=619636712&s=612x612&w=0&h=RlfRmp3IyN5GDmh_Gugxps7c_AYnBCk6nZgg3yf4H3c="
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    profileImageLocation = db.Column(db.String(500))
    
    sessions = db.relationship("SessionModel", lazy="dynamic") 
    activeSession = db.relationship("SessionModel", uselist=False, primaryjoin ="and_(UserModel.id==SessionModel.user_id, "
                                                        "SessionModel.active=='1')")
    tags = db.relationship("TagModel", lazy="dynamic")
    assets = db.relationship("AssetModel", lazy = "dynamic")
    def json(self):
        return {"email":self.email, "tags" : [tag.json() for tag in self.tags.all()], "assets" : [asset.json() for asset in self.assets.all()], "id" : self.id, "imageLocation" : self.profileImageLocation, "sessions" : [session.json() for session in self.sessions]}

    def __init__(self, firstname, lastname, email, password , profileImageLocation = defaultImage):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.profileImageLocation = profileImageLocation

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter(func.lower(UserModel.email) == func.lower(email)).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = int(id)).first()