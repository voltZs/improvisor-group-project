import os
from flask import Flask, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from resources.tag import Tag, TagList

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'UrMum'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/tag')
def tagUI(): #this throws an eror when it has the same name as the resource class (regardless of case) e.g def tag(): or def tagList():
    return render_template('something.html') 

api.add_resource(Tag, "/tagAPI")
api.add_resource(TagList, "/tagsAPI")
if __name__ =='__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)