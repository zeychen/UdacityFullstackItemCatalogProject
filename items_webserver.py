from flask import Flask, render_template
app = Flask(__name__)

# import database functions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from items_db_setup import Base, Categories, Items
from items_db_query import db_categories, db_items, db_category, db_item

# Create session and connect to DB
engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



#Fake category
# category = {'name': 'The CRUDdy Crab', 'id': '1'}

# categories = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake category items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','id':'3'},{'name':'Iced Tea', 'description':'with lemon','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese'}

# @app.route('/test')
# def test():
# 	items = session.query(Items).all()
# 	return render_template('categories.html', categories = items)



@app.route('/')
@app.route('/catalog/')
def allCategories():
	categories=db_categories(session)
	return render_template('categories.html', categories = categories)


@app.route('/<int:category_id>/items')
def allItems(category_id):
	category = db_category(session, category_id)
	items = db_items(session, category_id)
	# items = session.query(Items).filter_by(category_id=category.id).order_by(Items.name).all()
	# return "item = %s <br> category = %s" % (items, category)
	return render_template('items.html', items = items, category = category)


@app.route('/<int:category_id>/<int:item_id>/edit')
def editItem(category_id, item_id):
	category = db_category(session, category_id)
	item = db_item(session, item_id)
	# return "item = %s <br> category = %s" % (item, category)
	return render_template('edititem.html', category = category, item = item)


@app.route('/<int:category_id>/item/new')
def newItem(category_id):
	category = db_category(session, category_id)
	return render_template('newitem.html', category = category)


# @app.route('/<int:category_id>/<int:item_id>/delete')
# def deleteItem(category_name, item_name):
# 	return render_template('deleteitem.html', category = category, item = item)



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)