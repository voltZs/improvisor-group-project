from flask import Flask, render_template, request, redirect, abort, session
from improvisor import app, socketio, sample_files
from operator import itemgetter
import json
import copy

# Retrieve the sample assets from sample_files.py
assets = sample_files.assets


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/fetch_tagset', methods=['GET'])
def fetch_tagset():
    tag_pool = []
    for asset in assets:
        for tag in asset['tags']:
            if tag not in tag_pool:
                tag_pool.append(tag)
    return json.dumps(tag_pool)

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

@app.route('/assets', methods=['GET', 'POST'])
def asset_management_view():
    return render_template('asset_management.html')

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    pass

@app.route('/register', methods=['GET', 'POST'])
def register_view():
    return render_template('register.html')

@app.route('/compare_phrases', methods=['POST'])
def compare_phrases():

    recognised_tags = json.loads(request.form.get('recognisedTags'))
    mentioned_tags = request.form.get('mentionedTags')


    if not mentioned_tags:
        mentioned_tags = {'recent' : {},
                    'all' : {}
                }
    else:
        mentioned_tags = json.loads(mentioned_tags)

    # CREATE LIST OF ALL EXISTING TAGS ON ASSETS - THIS WOULD BE STORED OFC
    tag_pool = []
    for asset in assets:
        for tag in asset['tags']:
            if tag not in tag_pool:
                tag_pool.append(tag)

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
