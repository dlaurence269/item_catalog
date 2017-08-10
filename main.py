from flask import Flask, render_template, redirect, jsonify, url_for, request
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session


app = Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///beer_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# App Routing

# 1. Landing
@app.route('/') # GET - Landing page, directs routes to /beer
@app.route('/beers') # GET - List of all beer
def showAllBeers():
    categories = session.query(Category).order_by(asc(Category.name))
    
    query = session.query(Item)
    category_id_filter = request.args.get('category_id')
    if category_id_filter is not None:
        query = query.filter(Item.category_id == int(category_id_filter))
    
    print (query)
    items = query.all()
        # do something with the beers list

    return render_template('showAllBeers.html', categories=categories, items=items, Item=Item)

# 2. Show specific beer 
@app.route('/beers/<int:item_id>') # GET - See a specific item in detail
def showSpecificBeer(item_id):
    return render_template('showSpecificBeer.html')

# 3. New
# Add methods=['GET', 'POST']
@app.route('/beers/new') # GET - View to create a new item # POST - Create a new item
def newBeer():
    return render_template('newBeer.html')

# 4. Edit
# Add methods=['GET', 'POST']
@app.route('/beers/<int:item_id>/edit') # GET - View to edit a specific item # POST - Update a specific item
def editBeer(item_id):
    return render_template('editBeer.html')

# 5. Delete
# Add methods=['GET', 'POST']
@app.route('/beers/<int:item_id>/delete') # GET - View to delete a specific item (only if no popup) # POST - Delete a specific item
def deleteBeer(item_id):
    return render_template('deleteBeer.html')

# 6. Login
# Add methods=['GET', 'POST']
@app.route('/login') # GET - VView to login or signup # POST - Login via third party API
def login():
    return "This is the login page."

# 7. JSON all
@app.route('/beers/json') # GET - View JSON for all items (in alphabetical order)
def showAllBeersJSON():
    return "This is the view all beer in JSON page."

# 8. JSON specific item
@app.route('/beers/<int:item_id>/json') # GET - View JSON for a specific item
def showSpecificBeerJSON(item_id):
    return "This is the view JSON for a specific item page."


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
