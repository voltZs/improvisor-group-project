from db import db
from flask import session
from flask_login import current_user
from sqlalchemy import func

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def json(self):
        return {"tag" : self.tagname}

    def __init__(self, tagname, user_id):
        self.tagname = tagname.lower() #all tags will be made lowercase, doing it here means we don't have to worry about using .lower() anywhere else in our code 
        self.user_id = user_id
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_tagName(cls, tagname):
        lowerTagname = tagname.lower() #checking database for lower case version of argument. Doing it here for same reason as above
        return cls.query.filter_by(tagname=lowerTagname, user_id=current_user.get_id()).first()

    @classmethod
    def add_tag(cls, tagname):
        tags = cls.query.filter_by(user_id=current_user.get_id())
        
        found = False
        for tag in tags:
            if tag.tagname.lower() == tagname.lower():
                found = True
                return tag
        if not found:
            new_tag = TagModel(tagname, current_user.get_id())
            new_tag.save_to_db()
            return new_tag