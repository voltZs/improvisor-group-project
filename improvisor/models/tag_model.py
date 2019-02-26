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
        self.tagname = tagname
        self.user_id = user_id
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_tagName(cls, tagname):
        return cls.query.filter_by(tagname=tagname, user_id=current_user.get_id()).first()

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
            db.session.add(new_tag)
            db.session.commit()
            return new_tag