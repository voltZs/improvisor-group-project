from db import db

#association table
session_asset = db.Table ('session_asset', 
    db.Column("session_id", db.ForeignKey("sessions.id"), primary_key=True),
    db.Column("asset_id", db.ForeignKey("assets.id"), primary_key=True))