from flask_wtf import FlaskForm
from improvisor.forms import FormTag, FormSignup, FormAsset, FormLogin
from improvisor.models.tag_model import TagModel
from improvisor.models.user_model import UserModel
from improvisor.models.asset_model import AssetModel
from flask import Flask, render_template, request, redirect, jsonify, session
from improvisor import app

@app.route('/') 
def index():
    print("here")
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

#API: gets user from database and updates session dictionary
@app.route('/api/login', methods=["GET", "POST"])
def loginUser():
    form = FormLogin(request.form)
    if form.validate():
        print(f"valid form submitted {form.email.data} and {form.password.data}")
        user = UserModel.find_by_email(form.email.data)
        if user:
            session["user_id"] = user.id
            session["logged_in"] = True
            print(f'logged in as {user.email} with id {session["user_id"]}')
            return redirect('/')
        else:
            error = "Invalid credentials"
            return(render_template('login.html', form = form, error = error))
    print("form not valid")
    return (render_template('login.html', form= form))

#API: extracts all users from database
@app.route('/api/userList', methods=['GET'])
def getUsers():
    return jsonify({"users": [user.json() for user in UserModel.query.all()]})

#API: inserts asset into database and allows tags to be added to asset
@app.route('/api/asset', methods=["GET", "POST", "PUT"])
def addAsset():
    form = FormAsset(request.form)
    if (request.method=="POST" and form.validate()):
        print(f'Valid form submitted Asset-name is : {form.assetname}')
        if AssetModel.find_by_assetName(form.assetname):
            pass
            #return form back with message saying that an asset already exists with that name 
        if session["logged_in"] == True:
            asset = AssetModel(form.assetname, session["user_id"])
        else:
            pass
            #return form back with message saying that no user is logged in
        try:
            asset.save_to_db()
        except:
            error = "Error while saving asset to db"
            #return form back with error message
        