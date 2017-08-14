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
@app.route('/beers/<int:item_id>') # GET - See a specific item in detail
def showSpecificBeer(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('showSpecificBeer.html', item=item)

# 3. New
# GET - View to create a new item # POST - Create a new item
@app.route('/beers/new', methods=['GET', 'POST'])
def newBeer():
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'], 
                        price=request.form['price'], ibu=request.form['ibu'], abv=request.form['abv'],
                        category=request.form['category('')'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showAllBeers'))
    else:
        return render_template('newBeer.html')

# 4. Edit
# Add methods=['GET', 'POST']
@app.route('/beers/<int:item_id>/edit') # GET - View to edit a specific item # POST - Update a specific item
def editBeer(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('editBeer.html', item=item)

# 5. Delete
# Add methods=['GET', 'POST']
@app.route('/beers/<int:item_id>/delete') # GET - View to delete a specific item (only if no popup) # POST - Delete a specific item
def deleteBeer(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('deleteBeer.html', item=item)

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
