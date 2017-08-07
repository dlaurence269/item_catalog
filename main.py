from flask import Flask, render_template, redirect, jsonify, url_for
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session


app = Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///beers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# App Routing

# 1. Landing
@app.route('/') # GET - Landing page, directs routes to /beers
@app.route('/beers') # GET - List of all beers
def showBeers():
    return "This is the beers landing page."

# 2. Item in detail 
@app.route('/beers/<int:item_id>') # GET - See a specific item in detail
def showItemInDetail(item_id):
    return "This is a specific items' detailed page."

# 3. New
# Add methods=['GET', 'POST']
@app.route('/beers/new') # GET - View to create a new item # POST - Create a new item
def newBeer():
    return "This is the create new item page."

# 4. Edit
# Add methods=['GET', 'POST']
@app.route('/beers/<int:item_id>/edit') # GET - View to edit a specific item # POST - Update a specific item
def editBeer(item_id):
    return "This is the edit a specific item page."

# 4. Delete
# Add methods=['GET', 'POST']
@app.route('/beers/<int:item_id>/delete') # GET - View to delete a specific item (only if no popup) # POST - Delete a specific item
def deleteBeer(item_id):
    return "This is the delete a specific item page."

# 6. Login
# Add methods=['GET', 'POST']
@app.route('/login') # GET - VView to login or signup # POST - Login via third party API
def login():
    return "This is the login page."

# 7. JSON all
@app.route('/beers/json') # GET - View JSON for all items (in alphabetical order)
def showJSONAll():
    return "This is the view all beers in JSON page."

# 8. JSON specific item
@app.route('/beers/<int:item_id>/json') # GET - View JSON for a specific item
def showJSONItem(item_id):
    return "This is the view JSON for a specific item page."


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
