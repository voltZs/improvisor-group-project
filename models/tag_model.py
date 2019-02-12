from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(80))
    
    def json(self):
        return {"tag" : self.tagname}

    def __init__(self, tagname):
        self.tagname = tagname
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_tagName(cls, tagname):
        return cls.query.filter_by(tagname = tagname).first()