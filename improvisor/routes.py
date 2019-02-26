from flask_wtf import FlaskForm
from flask_wtf.file import FileField
import os, json, copy, bcrypt
from os.path import join
from improvisor.forms import FormTag, FormSignup, FormAsset, FormLogin
from improvisor.models.tag_model import TagModel
from improvisor.models.user_model import UserModel
from improvisor.models.asset_model import AssetModel
from flask import Flask, render_template, request, redirect, jsonify, session, abort, flash, url_for
from improvisor import app, socketio, sample_files, login_manager
from operator import itemgetter
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#API: inserts tag into database
@app.route('/api/tag', methods=['GET','POST'])
def addTag():
    form = FormTag(request.form)
    if (not current_user.is_authenticated): #A valid user must be logged in before a tag can be added to db
        print("No user is logged in. won't add tag")
        error ="User must be logged in to add a tag" #I don't really know how to use these error things for the flask forms Alex
        return render_template ("tag_form.html", form = form, error = error)

    if form.validate() and request.method=="POST":
        print("Valid form submitted: " + form.tag.data)
        tag = TagModel(form.tag.data, current_user.get_id()) #creates tag database object
        try:
            tag.save_to_db()
        except:
            error = "Error while saving to db"
            return render_template('tag_form.html', form=form, error=error)
        return redirect('/')
    return render_template('tag_form.html', form=form)


#API: extracts all of the current user's tags from the database returning a json
@login_required
@app.route('/api/user_tags_list', methods=['GET'])
def getTags():
    if current_user.is_authenticated:
        return jsonify({"tags":[tag.json() for tag in TagModel.query.filter_by(user_id=current_user.get_id()).all()]})
    else:
        print("No user is logged in, can't get tags")
        return redirect('/')


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


#API: returns all assets in the database
@app.route('/api/all_assets', methods=["GET"])
def allAssets():
    print("all_assets")
    return jsonify({"assets" : [asset.json() for asset in AssetModel.query.all()]})


#API: inserts asset into database and allows tags to be added to asset
@login_required
@app.route('/api/asset', methods=["GET", "POST"])
def addAsset():
    form = FormAsset()
    if request.method == "POST" and form.validate():
        print(f'Valid form submitted Asset-name is : {form.assetname.data}')

        asset = AssetModel.find_by_assetName(form.assetname.data) #tries to retrieve asset from database
        if asset:
            if form.tagname.data: #if the asset already exists then try to add a tag to it
                tags = form.tagname.data.split(",")
                print (tags)
                for tag in tags:
                    # If tag doesn't exist in tag list already then add it
                    tag_obj = TagModel.add_tag(tag)
                    asset.tags.append(tag_obj)
            else:
                print("asset already exists") #if no tag is entered then there is nothing to update
                flash("Asset already exists", "warning")
                return render_template("asset_form.html", form=form)
        else:
            asset = AssetModel(form.assetname.data, current_user.get_id())
            # need to remove extra white space. for example ('tag1', ' tag2')
            tags = form.tagname.data.split(",")
            print (tags)
            for tag in tags:
                # If tag doesn't exist in tag list already then add it
                tag_obj = TagModel.add_tag(tag)
                asset.tags.append(tag_obj)
        try:
            print(f'asset resource in addAsset is {form.assetResource.data}')
            upload(asset, form.assetResource.data, form.assetThumbnail.data)
        except Exception as e:
            print(e)
            flash("Error uploading file", "danger")
            return render_template("asset_form.html", form=form)
        try:
            asset.save_to_db()
        except:
            error = "Error while saving asset to db"
            return render_template("asset_form.html", form=form, error=error)
        flash("Successfully added asset", "success")
        return redirect('/api/asset')
    return render_template("asset_form.html", form=form)


def upload(asset, assetResource, assetThumbnail = None ):
    print ("saving upload")
    full_path = "improvisor/static/resources/uploadedFiles/user_" + str(current_user.get_id()) +"/"+ asset.assetname
    relative_path = url_for('static', filename='resources/uploadedFiles/')
    relative_path = relative_path + "user_" + str(current_user.get_id()) + "/" + asset.assetname
    print (f'assetResource is {assetResource}')
    if assetResource:
        print("saving asset Resource")
        save_location = full_path + "/" + assetResource.filename
        print (f'saving to {save_location}')
        if not os.path.exists(full_path):
            print("Making directory: " + full_path)
            os.makedirs(full_path)
        assetResource.save(save_location)
        asset.assetLocation = relative_path + "/" + assetResource.filename
    if assetThumbnail:
        save_location = full_path + "/" + assetThumbnail.filename
        assetThumbnail.save(save_location)
        asset.thumbnailLocation = relative_path + "/" + assetThumbnail.filename





@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/fetch_tagset', methods=['GET'])
def fetch_tagset():
    tag_pool = [tag.tagname for tag in current_user.tags]
    return json.dumps(tag_pool)

@app.route('/fetch_asset', methods=['GET'])
def fetch_asset():
    assets = [asset.json() for asset in current_user.assets.all()]
    id = int(request.args.get('id'))
    print(type(id))
    for asset in assets:
        if id == asset["id"]:
            return json.dumps(asset)
    return None

@app.route('/join_session', methods=['GET'])
def enter_session():
    return render_template('enter_session.html')


@app.route('/presenter', methods=['GET'])
def presenter_view():
    return render_template('presenter.html')


@app.route('/controller', methods=['GET'])
def controller_view():
    return render_template('controller.html')


@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings_view():
    return render_template('user_settings.html')


@app.route('/sessions', methods=['GET'])
def previous_sessions_view():
    return render_template('previous_sessions.html')


@login_required
@app.route('/assets/<id>', methods=['GET'])
def asset(id=None):
    if id is not None:
        asset = AssetModel.find_by_assetId(id)
        return render_template('asset_page.html', asset=asset)
    return render_template('asset_page.html', asset=None)


@login_required
@app.route('/assets/<id>/delete', methods=['POST'])
def asset_delete(id=None):
    if id is not None:
        # Delete the asset with id from db
        AssetModel.delete_by_assetId(id)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return json.dumps({'success':False}), 400, {'ContentType':'application/json'} 


@login_required
@app.route('/assets/<id>/update', methods=['POST'])
def asset_update(id=None):
    if id is not None:
        # Update the asset with id from db (not implemented yet)
        pass
    return json.dumps({'success':False}), 400, {'ContentType':'application/json'} 


@login_required
@app.route('/assets', methods=['GET', 'POST'])
def asset_management_view():
    user = UserModel.find_by_id(current_user.get_id())
    # Still need to sort by most recent THEN get first 20
    assets = user.assets[:20]
    return render_template('asset_management.html', assets=assets)


@login_required
@app.route('/assets/select', methods=['POST'])
def assets_select(search_tags=None, sorting=None, max_count=None):
    all_assets = []
    filter_tags = []
    match_count = 0

    user = UserModel.find_by_id(current_user.get_id())
    all_assets = user.assets

    for asset in all_assets:
        setattr(asset, 'tag_match_count', 0)
        if search_tags is not None:
            for search_tag in search_tags:
                if search_tag in asset.tags:
                    asset.tag_match_count += 1
            filter_tags.append(asset)
            match_count += 1
    
    sorted_assets = []
    
    # Not actually sure if this works yet, no particularly good way to test it
    if sorting.lower() == "recent":
        sorted_assets = sorted(filter_tags, key=itemgetter('dateCreated'))
    elif sorting.lower() == "old":
        sorted_assets = sorted(filter_tags, key=itemgetter('dateCreated'), reverse=True)
    elif sorting.lower() == "relevant":
        sorted_assets = sorted(filter_tags, key=itemgetter('tag_match_count'), reverse=True)

    output = []
    counter = 0
    for current in sorted_assets:
        if counter < max_count:
            output.append(current)
            counter += 1
        else:
            break

    return json.dumps(output)



@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = FormLogin(request.form)

    if request.method == "POST" and form.validate():
        user = UserModel.find_by_email(form.email.data)

        if user is not None and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
            login_user(user, remember = True)
            return redirect('/')
        else:
            flash('Invalid email or password', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session["selected_asset"] = ""
    return redirect('/')


@app.route('/signup', methods=['GET','POST'])
def signup_view():
    if current_user.is_authenticated:
        return redirect('/')

    form = FormSignup(request.form)
    if request.method == "POST" and form.validate():

        # Set the user inputs
		# Force only the initial character in first name to be capitalised
        first_name = (form.firstname.data.lower()).capitalize()

        # Make sure the first letter is capitalised. Don't care about capitalisation on the rest
        # Can't use .capitalize() here because it changes all other characters to lowercase
        last_name = form.lastname.data
        last_name_first_letter = last_name[0].capitalize()
        last_name_remaining_letters = last_name[1:]
        last_name = last_name_first_letter + last_name_remaining_letters

        email = form.email.data
        print(email, first_name, last_name)

        # Check if the email address already exists
        # (Need to make sure this is not case sensitive)
        user = UserModel.find_by_email(email)
        if user:
            flash('Account already exists', 'danger')
            return render_template('signup.html', form=form)
        else:
            # Encrypt the password using bcrypt
            hashpass = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
            # Make the new user using the user model
            user = UserModel(first_name, last_name, form.email.data, hashpass)
            try:
                user.save_to_db()

            except:
                flash('Error saving user to database', 'danger')
                return render_template('signup.html', form=form)
            addDirectory(user.id)
            return redirect("login")
    else:
        return render_template('signup.html', form=form)

def addDirectory(user_id):
    directory = join("improvisor/static/resources/uploadedFiles", "user_" + str(user_id))
    try:
        os.mkdir(directory)
    except:
        print("error making directory")


# Retrieve the sample assets from sample_files.py
#assets = sample_files.assets

@app.route('/compare_phrases', methods=['POST', "GET"])
def compare_phrases():
    assets = [asset.json() for asset in current_user.assets.all()]
    recognised_tags = json.loads(request.form.get('recognisedTags'))
    mentioned_tags = request.form.get('mentionedTags')

    if not mentioned_tags:
        mentioned_tags = {'recent' : {},
                    'all' : {}
                }
    else:
        mentioned_tags = json.loads(mentioned_tags)

    # CREATE LIST OF ALL EXISTING TAGS ON ASSETS - THIS WOULD BE STORED OFC
    tag_pool = [tag.tagname for tag in current_user.tags]
    # for asset in assets:
    #     for tag in asset['tags']:
    #         if tag not in tag_pool:
    #             tag_pool.append(tag)

    sorting_obj = {'assetResults' : {'current' : [],
                                    'frequent' :[]},
                'mentionedTags' : {}
            }

    # UPDATE THE MENTIONED_TAGS OBJECT
    for word in recognised_tags:
        # IF THE WORD IS NOT IN THE TAGS, INITIALISE - SSEPARATELY FOR RECENT AND ALL
        all_tags = mentioned_tags.get('all')
        recent_tags = mentioned_tags.get('recent')
        if not all_tags.get(word):
            mentioned_tags['all'][word] = {'mentions' : 0}
            print("Initialised mentioned_tags['all']['" + word + "]")
        if not recent_tags.get(word):
            mentioned_tags['recent'][word] = {'mentions' : 0}
            print("Initialised mentioned_tags['recent']['" + word + "]")

        # ADD THE NEW TAG TO THE MENTIONED_TAGS OBJ
        mentioned_tags['all'][word]['mentions'] += 1
        mentioned_tags['recent'][word]['mentions'] += 1
        print("Adding mention to " + word + " in  RECENT")
    # recent_tags = sortingObj.get(mentionedTags).get('recent')
    # session['recent']
    # sesssion['frequent']

    sorting_obj['mentionedTags'] = mentioned_tags

    frequent_assets = []
    current_assets = []

    # MANAGE ADDING asset_selection
    for asset in assets:
        ###### FOR ALL -> FREQUENT
        mentioned_all = mentioned_tags['all'].keys()
        asset['weight'] = 0
        # LOOP FOR UPDATING WEIGHT
        for tag in mentioned_all:
            if tag in asset['tags']:
                asset['weight'] += mentioned_tags['all'][tag]['mentions']
        # LOOP TO ADD FOUND ONES, BREAK SO IT ONLY ADDS ASSET ONCE IF
        # IT HAS MORE THAN ONE MATCHING TAG
        for tag in mentioned_all:
            if tag in asset['tags']:
                frequent_assets.append(asset)
                break

        #CREATE A COPY OF THE ASSET SO THE FREQUENT_ASSETS IS NOT OVERRIDEN
        asset2 = copy.copy(asset)
        ###### FOR RECENT -> CURRENT
        mentioned_recent = mentioned_tags['recent'].keys()
        asset2['weight'] = 0
        # LOOP FOR UPDATING WEIGHT
        for tag in mentioned_recent:
            if tag in asset2['tags']:
                asset2['weight'] += mentioned_tags['recent'][tag]['mentions']

        # LOOP TO ADD FOUND ONES, BREAK SO IT ONLY ADDS ASSET ONCE IF
        # IT HAS MORE THAN ONE MATCHING TAG
        for tag in mentioned_recent:
            if tag in asset2['tags']:
                current_assets.append(asset2)
                break

    sorted_frequent =  sorted(frequent_assets, key=itemgetter('weight'), reverse=True)
    sorted_current = sorted(current_assets, key=itemgetter('weight'), reverse=True)
    sorting_obj['assetResults']['frequent'] = sorted_frequent
    sorting_obj['assetResults']['current'] = sorted_current

    return json.dumps(sorting_obj)
