from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from flask import send_from_directory
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import datetime
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import os
from werkzeug import secure_filename



app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'images/uploads/'
# These are the extension that we are accepting to be uploaded
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Dream Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///dreamswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
# Route that will process the file upload
@app.route('/dreams/upload/', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
    # Get the name of the uploaded file
        file = request.files['file']
    # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
            return redirect(url_for('uploaded_file',
                                filename=filename))
    return render_template('upload.html')
    
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/dreams/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# Create a state token to prevent request forgery
# Store it in the session for later use
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        return resPaj('Invalid state parameter.', 401)
    access_token = request.data

    # Exchange client token for long-lived server-side token with GET
    # /oauth/access_token?grant_type=fb_exchange_token&client_id={app-
    # id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}
    app_id = json.loads(open('fb_client_secrets.json', 'r').read()
                        )['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read()
                            )['web']['app_secret']
    url = 'https://graph.facebook.com/v2.9/oauth/access_token?'\
          'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'\
          '&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print result

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.2/me"
    # strip expire tag from access token
    data = json.loads(result)
    token = 'access_token=' + data['access_token']

    url = 'https://graph.facebook.com/v2.8/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print 'new result:'
    print result

    data = json.loads(result)
    print data
    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data.get('email')
    if login_session['email'] is None:
        login_session['email'] = 'facebook@facebook.com'
    login_session['facebook_id'] = data['id']

    # Get user picture
    url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&'\
          'height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print 'result with pic:'
    print result
    data = json.loads(result)
    print data

    login_session['picture'] = data['data']['url']

    # check if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUserE(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 160px; height: 160px;'
    output += 'border-radius: 80px; -webkit-border-radius: 80px;'
    output += '-moz-border-radius: 80px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """Logout via Facebook OAuth."""
    facebook_id = login_session['facebook_id']

    # The access token must be included to successfully logout.
    access_token = login_session.get('access_token')

    url = ('https://graph.facebook.com/%s/permissions?'
           'access_token=%s') % (facebook_id, access_token)

    http = httplib2.Http()
    result = http.request(url, 'DELETE')[1]

    if result == '{"success":true}':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is'
                                            ' already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;"\
                "-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect/')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('access_token')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % credentials
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect/')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


# JSON APIs to view Dream Information
@app.route('/dreams/<int:category_id>/dream/JSON')
def dreamJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/dreams/<int:category_id>/dream/<int:item_id>/JSON')
def dreamItemJSON(category_id, item_id):
    Dream_Item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Dream_Item=Dream_Item.serialize)


@app.route('/dreams/JSON')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# Show Dream homepage
@app.route('/')
@app.route('/home/')
def homepage():
    return render_template('index.html')


# Show all categories
@app.route('/dreams/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return render_template('publiccategories.html', categories=categories)
    return render_template('privatecategories.html', categories=categories)


# Create new category
@app.route('/dreams/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'], description=request.form['description'],
            image=request.form['image'],
            user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New dream category %s successfully created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')


# Edit category
@app.route('/dreams/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCategory.user_id != login_session['user_id']:
        flash('You are not authorized to edit this category.'
              'Please create your own category to edit.')
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        if request.form['description']:
            editedCategory.description = request.form['description']
        if request.form['image']:
            editedCategory.image = request.form['image']
        flash('Category successfully edited %s' % editedCategory.name)
        return redirect(url_for('showCategories'))
    else:
        return render_template('editcategory.html', category=editedCategory)


# Delete category
@app.route('/dreams/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        flash('You are not authorized to delete this category.'
              ' Please create your own category to delete.')
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deletecategory.html',
                               category=categoryToDelete)


# Show items in category
@app.route('/dreams/<int:category_id>/')
@app.route('/dreams/<int:category_id>/dream/')
def showDreams(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    creator = getUserInfo(category.user_id)
    if 'username' not in login_session:
        return render_template('publicdreams.html', items=items,
                               category=category, creator=creator)
    else:
        return render_template('privatedreams.html', items=items,
                               category=category, creator=creator)


# Create new dream
@app.route('/dreams/<int:category_id>/dream/new/', methods=['GET', 'POST'])
def newDream(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
            newItem = Item(title=request.form['title'],
                           description=request.form['description'],
                           emotion=request.form['emotion'],
                           dream_date=datetime.datetime.strptime(
                           request.form['date'], '%Y-%m-%d'),
                           category_id=category_id,
                           user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            flash('New Dream Entry %s Successfully Created' % (newItem.title))
            return redirect(url_for('showDreams', category_id=category_id))
    else:
        return render_template('newdream.html', category_id=category_id)


# Edit dream
@app.route('/dreams/<int:category_id>/dream/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editDream(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != editedItem.user_id:
        flash('You are not authorized to edit this dream.'
              ' Please create your own dream to edit.')
        return redirect(url_for('showDreams', category_id=category_id))
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['emotion']:
            editedItem.emotion = request.form['emotion']
        if request.form['date']:
            editedItem.dream_date = datetime.datetime.strptime(
                                    request.form['date'], '%Y-%m-%d')
        session.add(editedItem)
        session.commit()
        flash('Dream Entry Successfully Edited')
        return redirect(url_for('showDreams', category_id=category_id))
    else:
        return render_template('editdream.html', category_id=category_id,
                               item_id=item_id, item=editedItem)


# Delete dream
@app.route('/dreams/<int:category_id>/dream/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteDream(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != itemToDelete.user_id:
        flash('You are not authorized to delete this dream. '
              'Please create your own dream to delete.')
        return redirect(url_for('showDreams', category_id=category_id))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Dream Entry Successfully Deleted')
        return redirect(url_for('showDreams', category_id=category_id))
    else:
        return render_template('deletedream.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
