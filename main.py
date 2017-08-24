from flask import Flask, render_template, redirect, jsonify, url_for, request
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session
import json
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2


app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///beer_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


########################
# Main App Routing
########################

# 1. Landing
# GET - All Beers
@app.route('/') # GET - Landing page, directs routes to /beer
@app.route('/beers') # GET - List of all beer
def showAllBeers():
    # Returns all Categories
    categories = session.query(Category).order_by(asc(Category.name))
    
    query = session.query(Item)
    category_id_filter = request.args.get('category_id')
    # If a Category is selected, return the beers within that category
    if category_id_filter is not None:
        query = query.filter(Item.category_id == int(category_id_filter))
    # Return results, if there is no category, all beers will show.
    print (query)
    items = query.all()
    # do something with the beers list
    return render_template('showAllBeers.html', categories=categories, items=items, Item=Item)

# 2. Show specific beer
# GET - See a specific item in detail
@app.route('/beers/<int:item_id>')
def showSpecificBeer(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('showSpecificBeer.html', item=item)

# 3. New
# GET - View to create a new item
# POST - Create a new item
@app.route('/beers/new', methods=['GET', 'POST'])
def newBeer():
    categories = session.query(Category).order_by(Category.id).all()
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'], 
                        picture_path=request.form['picture_path'], price=request.form['price'], 
                        ibu=request.form['ibu'], abv=request.form['abv'],
                        category_id=request.form['category_id'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showAllBeers'))
    else:
        return render_template('newBeer.html', categories=categories)

# 4. Edit
# GET - View to edit a specific item
# POST - Update a specific item
@app.route('/beers/<int:item_id>/edit', methods=['GET', 'POST'])
def editBeer(item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    categories = session.query(Category).order_by(Category.id).all()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['picture_path']:
            editedItem.course = request.form['picture_path']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['ibu']:
            editedItem.ibu = request.form['ibu']
        if request.form['abv']:
            editedItem.abv = request.form['abv']
        if request.form['category_id']:
            editedItem.category_id = request.form['category_id']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showAllBeers'))
    else:
        print (editedItem.category_id)
        return render_template('editBeer.html', item=editedItem, categories=categories)

# 5. Delete
# GET - View to delete a specific item (only if no popup)
# POST - Delete a specific item
@app.route('/beers/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteBeer(item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showAllBeers', item_id=item_id))
    else:
        return render_template('deleteBeer.html', item=itemToDelete)


########################
# JSON APIs to view Beer Information
########################

# 1. JSON Specific Beer
# GET - View JSON for a specific item
@app.route('/beers/<int:item_id>/json')
def showSpecificBeerJSON(item_id):
    specificBeer = session.query(Item).filter_by(id=item_id).one()
    return jsonify(specificBeer.serialize)
    #return "This is the view a specific item in JSON page."

# 2. JSON All Beers
# GET - View JSON for all items (in alphabetical order)
@app.route('/beers/json')
def showAllBeersJSON():
    allBeers = session.query(Item).all()
    return jsonify([b.serialize for b in allBeers])
    #return "This is the view all beers in JSON page."



#/**********************

########################
# OAuth, 3rd party login
########################

###
# Helper Methods
###
def json_response(message, status_code):
    response = make_response(json.dumps(messsage), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response

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

###
# Login Page
###
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    print ("The current session state is %s" % login_session['state'])
    return render_template('login.html', STATE=state)

###
# Begin Google Plus Sign-In
###
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        return json_response('Invalid state parameter.', 401)

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return json_response('Failed to upgrade the authorization code.', 401)

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        return json_response(result.get('error'), 500)

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return json_response("Token's user ID doesn't match given user ID.", 401)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        return json_response("Token's client ID does not match app's.", 401)

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        return json_response('Current user is already connected.', 200)

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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        return json_response('Current user not connected.', 401)

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return json_response('Successfully disconnected.', 200)

    else:
        return json_response('Failed to revoke token for given user.', 400)

#**********************/



if __name__ == '__main__':
    app.secret_key = 'super_secret_key' # Added for OAuth steps.
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
