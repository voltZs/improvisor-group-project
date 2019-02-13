import os
from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from resources.tag import Tag, TagList
from flask_wtf import FlaskForm
from forms import FormTag, FormSignup
from models.tag_model import TagModel

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'dearest_mother'


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tag_form', methods=['POST'])
def addTag():
    form = FormTag(request.form)
    if form.validate():
        print("Valid form submitted: " + form.tag.data)
        tag = TagModel(form.tag.data)
        try:
            tag.save_to_db()
        except:
            error = "Error while saving to db"
            return render_template('tag_form.html', form=form, error = error)
        return redirect('/')
    return render_template('tag_form.html', form=form)

@app.route('/tag_form', methods=['GET'])
def getTag():
    form = FormTag(request.form)
    return render_template('tag_form.html', form=form)

@app.route('/get_tags', methods=['GET'])
def getTags():
    return jsonify({"tags":[tag.json() for tag in TagModel.query.all()]})


if __name__ =='__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)