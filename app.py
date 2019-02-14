import os
from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from resources.tag import Tag, TagList
from flask_wtf import FlaskForm
from forms import FormTag, FormSignup
from models.tag_model import TagModel
from models.user_model import UserModel

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

#API: inserts tag into database
@app.route('/api/tag', methods=['GET','POST'])
def addTag():
    form = FormTag(request.form)
    if form.validate() and request.method=="POST":
        print("Valid form submitted: " + form.tag.data)
        tag = TagModel(form.tag.data, form.user_id.data)
        try:
            tag.save_to_db()
        except:
            error = "Error while saving to db"
            return render_template('tag_form.html', form=form, error = error)
        return redirect('/')
    return render_template('tag_form.html', form=form)

#API: extracts all tags from database
@app.route('/api/tagsList', methods=['GET'])
def getTags():
    return jsonify({"tags":[tag.json() for tag in TagModel.query.all()]})


#API: inserts user into database
@app.route('/api/userRegister', methods=['GET','POST'])
def addUser():
    form = FormSignup(request.form)
    if (request.method=="POST" and form.validate()):
        print(f'Valid form submitted Firstname: {form.firstname.data} Lastname: {form.lastname.data} Email: {form.email.data} ')
        user = UserModel(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
        try: 
            user.save_to_db()
        except: 
            error = "Error while saving user to db"
            return render_template('signup.html', form=form, error=error)
        return redirect('/')
    return render_template('signup.html', form=form)

#API: extracts all users from database
@app.route('/api/userList', methods=['GET'])
def getUsers():
    return jsonify({"users": [user.json() for user in UserModel.query.all()]})

if __name__ =='__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)