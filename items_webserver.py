from flask import Flask
app = Flask(__name__)

# import database functions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from items_db_setup import Base, Catagory, Item

# Create session and connect to DB
engine = create_engine('sqlite:///catagories.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catagories')
def allCatagories():
	return "This page will show all my catagories"


@app.route('/<string:catagories.name>/items')
def allItems():
	return "This page will show all items within a catagory"


@app.route('/<string:catagories.name>/item/new')
def newItem():
	return "This page will be for adding a new item to a catagory"


@app.route('/<string:catagories.name>/<string:item_catagory.name>/edit')
def editItem():
	return "This page will be for editing an item in a catagory"


@app.route('/<string:catagories.name>/<string:item_catagory.name>/delete')
def editItem():
	return "This page will be for deleting an item in a catagory"



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)