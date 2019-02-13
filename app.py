import os
from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api
from flask_cors import CORS
from resources.tag import Tag, TagList
from flask_wtf import FlaskForm
from forms import FormTag, FormSignup

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'dearest_mother'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tag')
def tagUI(): #this throws an eror when it has the same name as the resource class (regardless of case) e.g def tag(): or def tagList():
    return render_template('something.html') 


@app.route('/tag_form')
def tagform():
    form = FormTag(request.form)
    return render_template('tag_form.html', form=form) #only passing form because you were, don't know if you still need it after removing your code 


api.add_resource(Tag, "/tagAPI")
api.add_resource(TagList, "/tagsAPI")

if __name__ =='__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)