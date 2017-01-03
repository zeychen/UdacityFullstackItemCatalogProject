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

catagory_id = 2

@app.route('/')
@app.route('/catagories/')
def allCatagories():
	return "This page will show all catagories"


@app.route('/<string:catagory_name>/items')
def allItems(catagory_name):
	return "This page will show all items within a catagory"


@app.route('/<string:catagory_name>/item/new')
def newItem(catagory_name):
	return "This page will be for adding a new item to a catagory"


@app.route('/<string:catagory_name>/<string:item_name>/edit')
def editItem(catagory_name, item_name):
	return "This page will be for editing an item in a catagory"


@app.route('/<string:catagory_name>/<string:item_name>/delete')
def deleteItem(catagory_name, item_name):
	return "This page will be for deleting an item in a catagory"



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)