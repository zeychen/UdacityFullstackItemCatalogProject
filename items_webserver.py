from flask import Flask, render_template
app = Flask(__name__)

# import database functions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from items_db_setup import Base, Catagories, Items

# Create session and connect to DB
engine = create_engine('sqlite:///catagories.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catagories')
def allCatagories():
	return "This page will show all catagories"


@app.route('/<int:catagory_id>/items')
def allItems(catagories_id):
	return "This page will show all items within a catagory"


@app.route('/<int:catagory_id>/item/new')
def newItem(catagories_id):
	return "This page will be for adding a new item to a catagory"


@app.route('/<int:catagory_id>/<int:item_id>/edit')
def editItem(catagories_id, item_id):
	return "This page will be for editing an item in a catagory"


@app.route('/<int:catagory_id>/<int:item_id>/delete')
def deleteItem(catagories_id, item_id):
	return "This page will be for deleting an item in a catagory"



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)