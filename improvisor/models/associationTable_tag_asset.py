from db import db

#association table
asset_tags = db.Table ('asset_tags', 
    db.Column("asset_id", db.ForeignKey("assets.id"), primary_key=True),
    db.Column("tag_id", db.ForeignKey("tags.id"), primary_key=True))