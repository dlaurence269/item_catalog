from flask import Flask, render_template, redirect, jsonify, url_for, request
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session
import json


app = Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///beer_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# OAuth

# 1. Login
# GET - VView to login or signup
# POST - Login via third party API
# Add methods=['GET', 'POST']
@app.route('/login')
def login():
    return "This is the login page."


# JSON APIs to view Beer Information

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


# App Routing

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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
