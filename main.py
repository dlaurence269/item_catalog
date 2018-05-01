from flask import Flask, render_template, redirect, jsonify, url_for, request, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session
import json
import random
import string
import urllib
import requests


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
@app.route('/item_catalog/') # GET - Landing page, directs routes to /beer
@app.route('/item_catalog/beers') # GET - List of all beer
def showAllBeers():
    # User
    username = currentUserName()
    # Returns all Categories
    categories = session.query(Category).order_by(asc(Category.name))
    query = session.query(Item)
    category_id_filter = request.args.get('category_id')
    # If a Category is selected, return the beers within that category
    category_name = None
    if category_id_filter is not None:
        query = query.filter(Item.category_id == int(category_id_filter))
        category_name = session.query(Category).filter(Category.id == int(category_id_filter)).first().name
    # Return results, if there is no category, all beers will show
    print (query)
    items = query.all()
    # Do something with the beers list
    print (login_session)
    return render_template('showAllBeers.html', categories=categories, items=items,
                            Item=Item, category_name=category_name, isLoggedIn=isLoggedIn(),
                            isOwner=isOwner, username=username, currentUserName=currentUserName())

# 2. Show specific beer
# GET - See a specific item in detail
@app.route('/item_catalog/beers/<int:item_id>')
def showSpecificBeer(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    return render_template('showSpecificBeer.html', item=item, isLoggedIn=isLoggedIn(), 
                            isOwner=isOwner(item_id), currentUserName=currentUserName())

# 3. New
# GET - View to create a new item
# POST - Create a new item
@app.route('/item_catalog/beers/new', methods=['GET', 'POST'])
def newBeer():
    categories = session.query(Category).order_by(Category.id).all()
    if not isLoggedIn():
        return redirect('/')
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'], 
                        picture_path=request.form['picture_path'], price=request.form['price'], 
                        ibu=request.form['ibu'], abv=request.form['abv'],
                        category_id=request.form['category_id'], user_id=currentUserId())
        session.add(newItem)
        session.commit()
        flash('New Beer "%s" Successfully Created' % newItem.name)
        return redirect(url_for('showAllBeers'))
    else:
        return render_template('newBeer.html', categories=categories, isLoggedIn=isLoggedIn(), currentUserName=currentUserName())

# 4. Edit
# GET - View to edit a specific item
# POST - Update a specific item
@app.route('/item_catalog/beers/<int:item_id>/edit', methods=['GET', 'POST'])
def editBeer(item_id):
    editedItem = session.query(Item).filter_by(id=item_id).first()
    categories = session.query(Category).order_by(Category.id).all()
    if not isLoggedIn() or not isOwner(item_id):
        return redirect('/')
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
        flash('"%s" Successfully Edited' % editedItem.name)
        return redirect(url_for('showAllBeers'))
    else:
        print (editedItem.category_id)
        return render_template('editBeer.html', item=editedItem, categories=categories, 
                                isLoggedIn=isLoggedIn(), currentUserName=currentUserName())

# 5. Delete
# GET - View to delete a specific item (only if no popup)
# POST - Delete a specific item
@app.route('/item_catalog/beers/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteBeer(item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).first()
    if not isLoggedIn() or not isOwner(item_id):
        return redirect('/')
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('"%s" Successfully Deleted' % itemToDelete.name)
        return redirect(url_for('showAllBeers', item_id=item_id))
    else:
        return render_template('deleteBeer.html', item=itemToDelete, isLoggedIn=isLoggedIn(), currentUserName=currentUserName())


########################
# JSON APIs to view Beer Information
########################

# 1. JSON Specific Beer
# GET - View JSON for a specific item
@app.route('/item_catalog/beers/<int:item_id>/json')
def showSpecificBeerJSON(item_id):
    specificBeer = session.query(Item).filter_by(id=item_id).first()
    return jsonify(specificBeer.serialize)

# 2. JSON All Beers
# GET - View JSON for all items (in alphabetical order)
@app.route('/item_catalog/beers/json')
def showAllBeersJSON():
    allBeers = session.query(Item).all()
    return jsonify([b.serialize for b in allBeers])


########################
# OAuth, 3rd party login
########################

###
# Helper Methods
###
   
# Validate login
def currentUser():
    return login_session.get('user')

def currentUserName():
    if isLoggedIn():
        return currentUser().get('username')

def currentUserId():
    if isLoggedIn():
        return currentUser().get('id')

def isLoggedIn():
    return bool(currentUser())

# Validate user / owner
def isOwner(item_id):
    # Check who is the current User logged-in
    current_username = currentUserName()
    # Check which User created the item
    selectedItem = session.query(Item).filter_by(id=item_id).first()
    if selectedItem is None:
        return False
    item_user_id = selectedItem.user_id
    item_user = session.query(User).filter_by(id=item_user_id).first()
    # Check if the current User logged-in is the User that created the item
    return ((item_user is not None) and (item_user.username == current_username))


###
# Login Page
###
# click on login button to change state
# create a session so that username can be tracked
@app.route('/item_catalog/login', methods=['GET'])
def login():
    redirect_uri = urllib.parse.quote("http://daniellaurence.com/item_catalog/authorized")
    return redirect('http://github.com/login/oauth/authorize?client_id=Iv1.c9176e57e7b2b023&redirect_uri=' + redirect_uri)

    '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    print ("The current session state is %s" % login_session['state'])
    return render_template('login.html', STATE=state)
    '''

@app.route('/item_catalog/authorized', methods=['GET'])
def authorized():
    #make a POST request, remember dict == dictionary
    dictToSend = {'client_id':'Iv1.c9176e57e7b2b023',
                    'client_secret':'86d63fea4a2fd0e28163a312fd1e92b44a875553',
                    'code':request.args.get('code')}
    headers = {'accept':'application/json'}
    response = requests.post('https://github.com/login/oauth/access_token', json=dictToSend, headers=headers)
    print ('response from server:',response.text)
    dictFromServer = response.json()
    token = dictFromServer['access_token']
    return get_user_info(token)

    # GET request with access token to get user info
def get_user_info(token):
    headers = {'accept':'application/json'}
    response = requests.get('https://api.github.com/user?access_token='+token, headers=headers)
    print ('response from server:',response.text)
    # make this in to proper json, and parse out relevant information: username (login), and later ID
    github_user_info_dict = response.json()
    github_username = github_user_info_dict['login']
    # github_userid = github_user_info_dict['id']
    return use_or_create_user(github_username)

    # find or create on user model
    ## query to see if user exists, if not create one
def use_or_create_user(github_username):
    user = session.query(User).filter_by(username=github_username).first()
    if user is None:
        newUser = User(username=github_username)
        session.add(newUser)
        session.commit()
        flash('New User Successfully Added')
        user = newUser
    # set user in session
    login_session['user'] = user.serialize
    # redirect to home page
    return redirect(url_for('showAllBeers'))


@app.route('/item_catalog/logout', methods=['POST'])
def logout():
    login_session.pop('user', None)
    return redirect('/')


###
# Begin GitHub Sign-In
###


if __name__ == '__main__':
    app.secret_key = 'super_secret_key' # Added for OAuth steps.
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
