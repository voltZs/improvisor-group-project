from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from db import db
import os, json, copy, bcrypt
import base64
from os.path import join
from improvisor.forms import FormSession, FormTag, FormSignup, FormAsset, FormLogin, FormUpdateAsset, FormUpdateSettings, FormRequestPasswordReset, FormResetPassword
from improvisor.models.tag_model import TagModel
from improvisor.models.user_model import UserModel
from improvisor.models.asset_model import AssetModel
from improvisor.models.session_model import SessionModel
from improvisor.models.date_model import DateModel
from improvisor.models.associationTable_tag_asset import asset_tags
from improvisor.models.associationTable_session_asset import session_asset
from sqlalchemy import desc, asc
from flask import Flask, render_template, request, redirect, jsonify, session, abort, flash, url_for
from improvisor import app, login_manager, mail
from operator import itemgetter
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from PIL import Image, ExifTags
from datetime import datetime, date
import time
from json import dumps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message


@app.context_processor
def inject_active_session():
    if current_user.is_authenticated:
        active = SessionModel.find_active_session()
        if active:
            return dict(active=active)
        else:
            return dict(active=None)
    else:
        return dict(active=None)

@app.route('/api/session')
@login_required
def json_session():
    return jsonify({"sessionAssets": [session.json() for session in SessionModel.query.all()]})


#API: extracts all of the current user's tags from the database returning a json
@app.route('/api/user_tags_list', methods=['GET'])
@login_required
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


# #API: adds user profile picture to databas
# @app.route ('/api/profile_picture', methods =["GET", "POST"])
# @login_required


#     return render_template("user_profile.html", form = form)

#API: inserts asset into database and allows tags to be added to asset
@app.route('/assets/new', methods=["GET", "POST"])
@login_required
def addAsset():
    form = FormAsset()
    if request.method == "POST" and form.validate():
        print(f'Valid form submitted Asset-name is : {form.assetname.data}')
        asset = AssetModel(form.assetname.data, current_user.get_id(), form.assettype.data)
        tags = form.tagname.data.split(",")
        print(f'assettype is {form.assettype.data}')
        print (tags)
        for tag in tags:
            # Remove extra white space
            tag = " ".join(tag.split())
            if len(tag) > 0:
                tag_obj = TagModel.find_by_tagName(tag)
                if tag_obj is None: #then tag currently does not exist and needs to be added
                    tag_obj = TagModel(tag, current_user.get_id())
                    tag_obj.save_to_db()
                asset.tags.append(tag_obj)
        asset.assetLink =  form.assetLink.data
        try:
            print(f'asset resource in addAsset is {form.assetResource.data}')
            upload(asset, form.assetResource.data, form.assetAutomaticThumbnail.data, form.assetThumbnail.data)
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


def upload(asset, assetResource, thumbBase64, assetThumbnail = None ):
    print ("saving upload")
    full_path = "improvisor/static/resources/uploadedFiles/user_" + str(current_user.get_id()) +"/"+ asset.assetname
    relative_path = url_for('static', filename='resources/uploadedFiles/')
    relative_path = relative_path + "user_" + str(current_user.get_id()) + "/" + asset.assetname
    print (f'assetResource is {assetResource}')
    if asset.assettype == "file":
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
    elif thumbBase64:
        print("In thumbase64")
        save_location = full_path + "/Thumb" + assetResource.filename
        #removes the description from the string
        thumbBase64 = thumbBase64.replace("data:image/png;base64,", '')
        image = base64.b64decode(thumbBase64 + "==")
        with open(save_location, 'wb') as f:
            f.write(image)
        asset.thumbnailLocation = relative_path + "/Thumb" + assetResource.filename





@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/fetch_tagset', methods=['GET'])
@login_required
def fetch_tagset():
    tag_pool = [tag.tagname for tag in current_user.tags]
    return json.dumps(tag_pool)

@app.route('/fetch_asset', methods=['GET'])
@login_required
def fetch_asset():
    id = int(request.args.get('id'))
    asset = {}
    if id is not None:
        asset = AssetModel.find_by_assetId(id).json()
        # asset.pop("date-created", None)
        # asset.pop("dateAdded", None)
        # date time objects are being removed because they're not JSON serializable..
        return dumps(asset, default = json_serial)
    return None

@app.route('/new_session', methods=['GET'])
@login_required
def new_session():
    # Check if the active session has any assets in it
    # If it has no assets then don't create a new session
    session = SessionModel.find_active_session()
    if session == None or len(session.assets) > 0:
        new_session = SessionModel()
        new_session.save_to_db()
        return render_template('enter_session.html', mode="new")
    else:
        session.remove_from_db()
        new_session = SessionModel()
        new_session.save_to_db()
        return render_template('enter_session.html', mode="empty")

@app.route('/continue_session', methods=['GET'])
@login_required
def continue_session():
    # Make sure a session is already active. If not then create a new one
    session = SessionModel.find_active_session()
    if session == None:
        flash("No active session. A new session was created", "warning")
        return redirect('/new_session')
    return render_template('enter_session.html', mode="continue")

@app.route('/presenter', methods=['GET'])
@login_required
def presenter_view():
    return render_template('presenter.html')

@app.route('/controller', methods=['GET'])
@login_required
def controller_view():
    session = SessionModel.find_active_session()
    if session:
        return render_template('controller.html')
    else:
        return redirect('/new_session')

@app.route('/fetch_active_session_assets', methods=['GET'])
@login_required
def fetch_active_session_assets():
    session = SessionModel.find_active_session()
    if session:
        dates = get_full_session(session)
        return jsonify({"assets" : [date.json() for date in dates]})
    else:
        return dumps([])

@app.route('/user_settings', methods=['GET', 'POST'])
@login_required
def user_settings_view():
    form = FormUpdateSettings()
    if form.validate() and request.method == "POST" and current_user.is_authenticated:
        print("form valid")
        if form.userPicture.data:
            addPicture(form)
        if form.passwordUpdate.data:
            hashpass = bcrypt.hashpw(form.passwordUpdate.data.encode('utf-8'), bcrypt.gensalt())
            current_user.password = hashpass
            current_user.save_to_db()
        if form.emailUpdate.data:
            current_user.email = form.emailUpdate.data
            current_user.save_to_db()
    return render_template('user_settings.html', form = form)


def addPicture(settingsForm):
    form = settingsForm
    relative_path = url_for('static', filename='resources/uploadedFiles/')
    relative_path = relative_path + "user_" + str(current_user.get_id())
    full_path = "improvisor/static/resources/uploadedFiles/user_" + str(current_user.get_id())
    save_location = full_path + "/" + form.userPicture.data.filename
    filename = form.userPicture.data.filename
    image_user = Image.open(form.userPicture.data)

    #looks at image metadata to check for a camera orientation and then rotates it appropriately so it appears the right way round in html display
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(image_user._getexif().items())
        print(exif[orientation])
        if exif[orientation] == 3 :
            image_user2 = image_user.resize((120,120), Image.ANTIALIAS )
            image_user2.rotate(180, expand=True).save(save_location)
        elif exif[orientation] == 6 :
            image_user2 = image_user.resize((120,120), Image.ANTIALIAS )
            image_user2.rotate(270, expand=True).save(save_location)
        elif exif[orientation] == 8 :
            image_user2 = image_user.resize((120,120), Image.ANTIALIAS )
            image_user2.rotate(90, expand=True).save(save_location)


    except Exception as e:
        print(e)
        image_user.save(save_location)
    if (current_user.profileImageLocation != "https://media.istockphoto.com/photos/portrait-of-a-businessman-picture-id619636712?k=6&m=619636712&s=612x612&w=0&h=RlfRmp3IyN5GDmh_Gugxps7c_AYnBCk6nZgg3yf4H3c="):
        os.remove("improvisor" + current_user.profileImageLocation)
    current_user.profileImageLocation = relative_path + "/" + filename
    db.session.commit()

@app.route('/sessions', methods=['GET'])
@login_required
def previous_sessions_view():
    sessions = SessionModel.find_all_sessions()
    return render_template('previous_sessions.html', sessions=sessions)


@app.route('/sessions/<id>', methods=['GET'])
@login_required
def session_page(id=None):
    if id != None:
        session = SessionModel.find_by_sessionNumber(id)
        if session != None:
            form = FormSession()
            custom_session = copy.deepcopy(session)
            dates = get_full_session(session)
            setattr(custom_session, "dates", [date.json() for date in dates])
            return render_template('session.html', session=custom_session, form=form)
    return redirect('/sessions')


# Returns a session with ALL occurences of the assets in it, including duplicates
def get_full_session(session):
    dateList = []
    for asset in session.assets:
        for dateObj in asset.get_dates_for_session(session.sessionNumber):
            dateList.append(dateObj)
    dateList.sort(key=lambda x : x.dateAdded)
    return dateList

@app.route('/sessions/<id>/delete', methods=['POST'])
@login_required
def session_delete(id=None):
    if id is not None:
        # Delete the session with number <id> from db
        print(id)
        session = SessionModel.find_by_sessionNumber(id)
        print(type(session))
        session.remove_from_db()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return json.dumps({'success':False}), 400, {'ContentType':'application/json'}


@app.route('/assets', methods=['GET', 'POST'])
@login_required
def asset_management_view():
    user = UserModel.find_by_id(current_user.get_id())
    # desc => from most recent to oldest
    assets = user.assets.order_by(desc(AssetModel.dateCreated)).limit(10).all()
    return render_template('asset_management.html', assets=assets)

@app.route('/assets/bulk_delete', methods=['POST'])
@login_required
def assets_bulk_delete():
    idList = json.loads(request.form.get('idList'));
    deleted = []
    if idList is not None:
        for id in idList:
            # Delete the asset with id from db
            AssetModel.delete_by_assetId(id)
            deleted.append(id)
    return json.dumps(deleted)

@app.route('/assets/select', methods=['POST'])
@login_required
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
    if not (filter_tags == None or len(filter_tags) == 0):
        for asset in unfiltered:
            for filter_tag in filter_tags:
                if filter_tag in asset['tags']:
                    filtered.append(asset)
                    # move on to next asset
                    break
    else:
        print("here")
        filtered = unfiltered

    sorted_assets = []

    # sorting
    if sorting.lower() == "recent":
        sorted_assets = sorted(filtered, key=itemgetter('date-created'), reverse=True)
    elif sorting.lower() == "old":
        sorted_assets = sorted(filtered, key=itemgetter('date-created'), reverse=False)
    elif sorting.lower() == "relevant":
        assets_match_count =[]
        for asset in filtered:
            asset['tag_match_count']= 0
            if not (filter_tags is None or len(filter_tags) == 0):
                for filter_tag in filter_tags:
                    if filter_tag in asset['tags']:
                        asset['tag_match_count'] += 1
            assets_match_count.append(asset)
        sorted_assets = sorted(assets_match_count, key=itemgetter('tag_match_count'), reverse=True)
    sorted_assets = sorted_assets[0:limit]
    return dumps(sorted_assets, default=json_serial)


#anything that has /asset/... needs to be before /asset/<id>
@app.route('/assets/<id>', methods=['GET'])
@login_required
def asset(id=None):
    form = FormUpdateAsset()
    if id is not None:
        asset = AssetModel.find_by_assetId(id)
        return render_template('asset_page.html', asset=asset, form= form)
    return render_template('asset_page.html', asset=None, form = form)

@app.route('/assets/<id>/delete', methods=['POST'])
@login_required
def asset_delete(id=None):
    if id is not None:
        # Delete the asset with id from db
        AssetModel.delete_by_assetId(id)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

@app.route('/assets/<id>/update', methods=['GET', 'POST'])
@login_required
def asset_update(id=None):
    if id is not None:
        form = FormUpdateAsset(request.form)
        asset = AssetModel.find_by_assetId(id)

        if form.validate():
            print("validated form update")
            tag_array = form.tagArrayString.data
            tag_array = tag_array.split(',')
            tag_array = [x.lower() for x in tag_array]
            existing_tags =[item.tagname.lower() for item in asset.tags]
            for tag in tag_array:
                if len(tag) > 0:
                    if not tag in existing_tags: # if the tag does not exist in the asset add it
                        new_tag = TagModel.add_tag(tag)
                        asset.tags.append(new_tag);
                        print("added tag " + tag)
                        asset.save_to_db()
                # if tag already exists in the asset, do nothing

            for existing_tag in existing_tags:
                if not existing_tag in tag_array: #if existing tag is not in the new tag_array, delete it
                    tag_to_delete = TagModel.add_tag(existing_tag)
                    asset.tags.remove(tag_to_delete)
                    print("deleted tag " + existing_tag)
                    asset.save_to_db()
                #if existing tag is present in the new tag_array keep it
            if form.thumbnailLocation.data:
                asset.thumbnailLocation = form.thumbnailLocation.data;
                asset.save_to_db()
            

    return redirect(url_for('asset', id=id))



@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

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


# Generate a password reset token that lasts 30 minutes
def get_reset_token(self, expires_sec=1800):
	s = Serializer(app.secret_key, expires_sec)
	return s.dumps({'_id' : str(self.id)}).decode('utf-8')


# Send an email containing the password reset token
def send_reset_email(user):
	token = get_reset_token(user)
	reset_url = url_for('reset_token', token=token, _external=True)

	subject = 'Improvisor | Password Reset Request'
	template = render_template('email.html', reset_url=reset_url, user=user)
	msg = Message(
		subject,
		sender='noreply.improvisor@gmail.com',
		recipients=[user.email],
		html = template)

	mail.send(msg)


# Verify the password reset token is valid
def verify_reset_token(token):
    s = Serializer(app.secret_key)
    try:
        user_id = s.loads(token)['_id']
    except:
        return None
    return UserModel.find_by_id(user_id)


@app.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    form = FormRequestPasswordReset()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = UserModel.find_by_email(email)

        if user is None:
            error = "wrong_email"
            return render_template('password_reset_request.html', form=form, error=error)
        else:
            print("Request password reset for ", email)
            send_reset_email(user)
            flash('Password reset email has been sent!', 'info')
            return redirect(url_for('login'))

    return render_template('password_reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
	user = verify_reset_token(token)
	if user is None:
		flash('Invalid or expired reset token.', 'danger')
		return redirect(url_for('reset_request'))
	else:
		form = FormResetPassword()
		if request.method == 'POST' and form.validate():

			hashpass = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
			# Update the current user password
			user.password = hashpass
			user.save_to_db()

			print("INFO: Password Reset for", user.email)
			flash('Password has been reset!', 'success')
			return redirect(url_for('login'))

		return render_template('password_reset_form.html', form=form)


@app.route('/compare_phrases', methods=['POST', 'GET'])
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
        # asset.pop('date-created', None)
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

    return dumps(sorting_obj, default=json_serial)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

# howdy partner