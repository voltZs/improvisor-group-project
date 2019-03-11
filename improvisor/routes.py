from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from db import db
import os, json, copy, bcrypt
from os.path import join
from improvisor.forms import FormTag, FormSignup, FormAsset, FormLogin, FormProfilePicture, FormUpdateAsset
from improvisor.models.tag_model import TagModel
from improvisor.models.user_model import UserModel
from improvisor.models.asset_model import AssetModel
from improvisor.models.associationTable_tag_asset import asset_tags
from sqlalchemy import desc, asc
from flask import Flask, render_template, request, redirect, jsonify, session, abort, flash, url_for
from improvisor import app, login_manager
from operator import itemgetter
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from PIL import Image, ExifTags

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

#API: returns all assets in the database
@app.route('/api/all_assets', methods=["GET"])
def allAssets():
    print("all_assets")
    return jsonify({"assets" : [asset.json() for asset in AssetModel.query.all()]})

#API: adds user profile picture to database
@app.route ('/api/profile_picture', methods =["GET", "POST"])
def addPicture():
    print (os.getcwd())
    form = FormProfilePicture()
    if request.method == "POST" and form.validate() and current_user.is_authenticated:
        relative_path = url_for('static', filename='resources/uploadedFiles/')
        relative_path = relative_path + "user_" + str(current_user.get_id()) 
        full_path = "improvisor/static/resources/uploadedFiles/user_" + str(current_user.get_id()) 
        save_location = full_path + "/" + form.userPicture.data.filename


        #form.userPicture.data.save(save_location)
        
        filename = form.userPicture.data.filename
        print(type(filename))
        image_user = Image.open(form.userPicture.data)
       
        #looks at image metadata to check for a camera orientation and then rotates it appropriately so it appears the right way round in html display 
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation': 
                    break
            exif=dict(image_user._getexif().items())
            print(exif[orientation])
            if exif[orientation] == 3 : 
                image_user2=image_user.rotate(180, expand=True)
            elif exif[orientation] == 6 : 
                image_user2=image_user.rotate(270, expand=True)
            elif exif[orientation] == 8 : 
                print("rotating")
                image_user2=image_user2.rotate(90, expand=True)
                
        except Exception as e:
            print(e)
        
            
        image_user2 = image_user.resize((120,120), Image.ANTIALIAS )
        image_user2.save(save_location)
        current_user.profileImageLocation = relative_path + "/" + filename
        db.session.commit()

        


    return render_template("user_profile.html", form = form)

#API: inserts asset into database and allows tags to be added to asset
@login_required
@app.route('/assets/new', methods=["GET", "POST"])
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
                    # Remove extra white space
                    tag = " ".join(tag.split())
                    tag_obj = TagModel.find_by_tagName(tag)
                    print(f'tag found {tag_obj.json()}')
                    if tag_obj is None: #then tag currently does not exist and needs to be added
                        tag_obj = TagModel(tag, current_user.get_id())
                        tag_obj.save_to_db()
                        asset.tags.append(tag_obj)
      
            else:
                print("asset already exists") #if no tag is entered then there is nothing to update
                flash("Asset already exists", "warning")
                return render_template("asset_form.html", form=form)
        else:
            asset = AssetModel(form.assetname.data, current_user.get_id())
            tags = form.tagname.data.split(",")
            print (tags)
            for tag in tags:
                # Remove extra white space
                tag = " ".join(tag.split())
                tag_obj = TagModel.find_by_tagName(tag)
                if tag_obj is None: #then tag currently does not exist and needs to be added
                    tag_obj = TagModel(tag, current_user.get_id())
                    tag_obj.save_to_db()
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
        return redirect('/assets/new')
    else:
        print("Not a form")
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
    id = int(request.args.get('id'))
    asset = {}
    if id is not None:
        asset = AssetModel.find_by_assetId(id).json()
        asset.pop("date-created", None)
        return json.dumps(asset)
    return None


@app.route('/join_session', methods=['GET'])
def enter_session():
    return render_template('enter_session.html')


@login_required
@app.route('/presenter', methods=['GET'])
def presenter_view():
    return render_template('presenter.html')


@login_required
@app.route('/controller', methods=['GET'])
def controller_view():
    return render_template('controller.html')


@login_required
@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings_view():
    return render_template('user_settings.html')


@app.route('/sessions', methods=['GET'])
def previous_sessions_view():
    return render_template('previous_sessions.html')


@login_required
@app.route('/assets', methods=['GET', 'POST'])
def asset_management_view():
    user = UserModel.find_by_id(current_user.get_id())
    # desc => from most recent to oldest
    assets = user.assets.order_by(desc(AssetModel.dateCreated)).limit(10).all()
    return render_template('asset_management.html', assets=assets)


@login_required
@app.route('/assets/bulk_delete', methods=['GET'])
def assets_bulk_delete():
    idList = request.form.get('idList')
    deleted = []
    if idList is not None:
        for id in idList:
            # Delete the asset with id from db
            AssetModel.delete_by_assetId(id)
            deleted.append(id)
    return json.dumps(deleted)


@login_required
@app.route('/assets/select', methods=['POST'])
def assets_select():
    filter_tags = request.form.get('filterTags')
    # possible values: RECENT, OLD, RELEVANT
    sorting = request.form.get('sorting')
    limit = request.form.get('limit')

    if filter_tags:
        filter_tags = json.loads(filter_tags)

    if sorting:
        if not (sorting.lower() == "recent" or sorting.lower() == "old" or sorting.lower() == "relevant"):
            sorting = "recent"
    else:
        sorting = "recent"

    if limit:
        limit = int(limit)
    else:
        limit = 10

    # filtering
    unfiltered = [asset.json() for asset in UserModel.find_by_id(current_user.get_id()).assets.all()]
    filtered = []
    if not (filter_tags is None or filter_tags == []):
        for asset in unfiltered:
            for filter_tag in filter_tags:
                if filter_tag in asset['tags']:
                    filtered.append(asset)
                    # move on to next asset
                    break
    else:
        filtered = unfiltered

    sorted_assets = []

    # sorting
    if sorting.lower() == "recent":
        sorted_assets = sorted(filtered, key=itemgetter('date-created'), reverse=True)
        sorted_assets = sorted_assets[0:limit]
    elif sorting.lower() == "old":
        sorted_assets = sorted(filtered, key=itemgetter('date-created'), reverse=False)
        sorted_assets = sorted_assets[0:limit]
    elif sorting.lower() == "relevant":
        assets_match_count =[]
        match_count = 0
        for asset in filtered:
            if match_count < limit:
                asset['tag_match_count']= 0
                if not (filter_tags is None or filter_tags == []):
                    for filter_tag in filter_tags:
                        if filter_tag in asset['tags']:
                            asset['tag_match_count'] += 1
                    assets_match_count.append(asset)
                    match_count += 1
            else:
                break
        sorted_assets = sorted(assets_match_count, key=itemgetter('tag_match_count'), reverse=True)
    [asset.pop('date-created', None) for asset in sorted_assets]
    return json.dumps(sorted_assets)


#anything that has /asset/... needs to be before /asset/<id>
@login_required
@app.route('/assets/<id>', methods=['GET'])
def asset(id=None):
    form = FormUpdateAsset()
    if id is not None:
        asset = AssetModel.find_by_assetId(id)
        return render_template('asset_page.html', asset=asset, form= form)
    return render_template('asset_page.html', asset=None, form = form) 


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
    #known issue: tags can be added multiple times 
    if id is not None:
        form = FormUpdateAsset()
        asset = AssetModel.find_by_assetId(id)
        print(asset.tags)
        if form.validate():
            print(f"valid form {form.tagname.data} {form.operation.data}")
            tag = TagModel.add_tag(form.tagname.data)
            if tag and form.operation.data == "delete":
                print("delete operation")
                if tag in asset.tags:
                    asset.tags.remove(tag)
                    asset.save_to_db()
                else:
                    flash(f"asset {asset.assetname} does not have that tag (1)", "danger") #when the user has this tag on their account but the asset does not contain it
                    return render_template("asset_page.html", form = form, asset= asset)
            elif form.operation.data == "add":
                print("add operation")
                if tag not in asset.tags:
                    asset.tags.append(tag)
                    asset.save_to_db()
                else:
                    flash("Asset already has the tag '" + tag.tagname  +"'", "warning")
                return render_template("asset_page.html", form = form, asset= asset)
            else:
                flash(f"asset {asset.assetname} does not have that tag (2)", "danger") #when the tag selected for deletion does not exist on the user's account or no operation radio button was selected
                return render_template("asset_page.html", form = form, asset= asset)
        return render_template("asset_page.html", form = form, asset= asset)
    return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

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
        asset.pop('date-created', None)
        print(asset)
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
