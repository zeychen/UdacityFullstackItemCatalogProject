from flask import Flask, render_template
app = Flask(__name__)

# import database functions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from items_db_setup import Base, Catagories, Items
from items_db_query import db_catagories, db_items

# Create session and connect to DB
engine = create_engine('sqlite:///catagories.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



#Fake catagory
# catagory = {'name': 'The CRUDdy Crab', 'id': '1'}

# catagories = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake catagory items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','id':'3'},{'name':'Iced Tea', 'description':'with lemon','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese'}





@app.route('/')
@app.route('/catalog/')
def allCatagories():
	catagories=db_catagories(session)
	return render_template('catagories.html', catagories = catagories)


@app.route('/<string:catagory_name>/items')
def allItems(catagory_name):
	catagory = db_catagories(session)
	items = db_items(session, catagory_name)
	return render_template('items.html', items = items, catagory = catagory)


@app.route('/<string:catagory_name>/item/new')
def newItem(catagory_name):
	catagory = db_catagory(session, catagory_name)
	return render_template('newitem.html', catagory = catagory)


@app.route('/<string:catagory_name>/<string:item_name>/edit')
def editItem(catagory_name, item_name):
	return render_template('edititem.html', catagory = catagory, item = item)


@app.route('/<string:catagory_name>/<string:item_name>/delete')
def deleteItem(catagory_name, item_name):
	return render_template('deleteitem.html', catagory = catagory, item = item)



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)