from flask_wtf import FlaskForm
from improvisor.forms import FormTag, FormSignup, FormAsset, FormLogin
from improvisor.models.tag_model import TagModel
from improvisor.models.user_model import UserModel
from improvisor.models.asset_model import AssetModel
from flask import Flask, render_template, request, redirect, jsonify, session
from improvisor import app

@app.route('/') 
def index():
    return render_template('index.html')

#API: inserts tag into database
@app.route('/api/tag', methods=['GET','POST'])
def addTag():
    form = FormTag(request.form)
    if (session["logged_in"] == False): #A valid user must be logged in before a tag can be added to db
        print("No user is logged in. won't add tag")
        error ="User must be logged in to add a tag" #I don't really know how to use these error things for the flask forms Alex
        return render_template ("tag_form.html", form = form, error = error)
    
    if form.validate() and request.method=="POST":
        print("Valid form submitted: " + form.tag.data)
        tag = TagModel(form.tag.data, session["user_id"]) #creates tag database object
        try:
            tag.save_to_db()
        except:
            error = "Error while saving to db"
            return render_template('tag_form.html', form=form, error = error)
        return redirect('/')
    return render_template('tag_form.html', form=form)

#API: extracts all of the current user's tags from the database returning a json 
@app.route('/api/user_tags_list', methods=['GET'])
def getTags():
    if session["logged_in"] == True:
        return jsonify({"tags":[tag.json() for tag in TagModel.query.filter_by(user_id = session["user_id"]).all()]})
    else:
        print("No user is logged in, can't get tags")
        return redirect('/')


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

#API: gets user from database and updates session dictionary -- not secure yet
@app.route('/api/login', methods=["GET", "POST"])
def loginUser():
    form = FormLogin(request.form)
    if (request.method == "POST" and form.validate()):
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
    return (render_template('login.html', form= form))

#API: extracts all users from database
@app.route('/api/userList', methods=['GET'])
def getUsers():
    return jsonify({"users": [user.json() for user in UserModel.query.all()]})

#API: given a tag, returns a list of the user's assets containing that tag
@app.route('/api/assets_with_tag', methods=['GET'])
def getAssets():
    phrase = request.form.get('phrase')
    mentioned_tags = request.form.get("mentionedTags")
    tag = TagModel.find_by_tagName(phrase)
    if tag:
        return {"assets-with-tag" : [asset.json() for asset in tag.assets]}
    else: 
        return {"message" : "Tag does not exist in database"}
    #if not mentioned_tags:
        #mentioned_tags = {"recent" : {},
           # }

#API: returns all assets in the database
@app.route('/api/all_assets', methods=["GET"])
def allAssets():
    print("all_assets")
    return jsonify({"assets" : [asset.json() for asset in AssetModel.query.all()]})

#API: inserts asset into database and allows tags to be added to asset
@app.route('/api/asset', methods=["GET", "POST"])
def addAsset():
    form = FormAsset(request.form)
    if (session["logged_in"] == False): #A valid user must be logged in before an asset can be added to db
        print("No user is logged in. won't add asset")
        error ="User must be logged in to add a asset" 
        return render_template ("asset_form.html", form = form, error = error)

    if (request.method=="POST" and form.validate()):
        print(f'Valid form submitted Asset-name is : {form.assetname.data}')
        
        asset = AssetModel.find_by_assetName(form.assetname.data) #tries to retrieve asset from database
        if asset:   
            if form.tagname.data: #if the asset already exists then try to add a tag to it
                print (form.tagname.data)
                tag = TagModel.find_by_tagName(form.tagname.data)
                if tag:
                    asset.tags.append(tag)
            else:
                print("asset already exists") #if no tag is entered then there is nothing to update 
                return render_template("asset_form.html", form=form)
        else:
             asset = AssetModel(form.assetname.data, session["user_id"]) #if there is no asset in database then create it and check for possible tag entry 
             if form.tagname.data:
                tag = TagModel.find_by_tagName(form.tagname.data)
                if tag:
                    asset.tags.append(tag)
        try:
            asset.save_to_db()
        except:
            error = "Error while saving asset to db"
            return render_template("asset_form.html", form=form, error=error)
        return redirect('/')
    return render_template("asset_form.html", form=form )
    
        