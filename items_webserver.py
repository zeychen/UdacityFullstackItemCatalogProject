from flask import Flask, render_template, request, redirect, url_for, flash
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
	return render_template('items.html', items = items, category = category)


@app.route('/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
	"""
	edit items within category
	"""
	if request.method == 'POST':
		item = db_item(session, item_id)
		item.name = request.form['name']
		item.description = request.form['description']
		session.commit()
		return redirect(url_for('allItems', category_id=category_id))
	else:
		category = db_category(session, category_id)
		item = db_item(session, item_id)
		return render_template('edititem.html', category = category, item = item, name=item.name, description=item.description)


@app.route('/<int:category_id>/item/new', methods=['GET', 'POST'])
def newItem(category_id):
	if request.method == 'POST':
		newItem = Items(name=request.form['name'], description=request.form['description'], category_id = category_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('allItems', category_id=category_id))
	else:
		category = db_category(session, category_id)
		return render_template('newitem.html', category = category)


@app.route('/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
	if request.method == 'POST':
		item = db_item(session, item_id)
		session.delete(item)
		session.commit()
		return redirect(url_for('allItems', category_id=category_id, item_id=item_id))
	else:
		item = db_item(session, item_id)
		category = db_category(session, category_id)
		return render_template('deleteItem.html', category = category, item = item, name=item.name, description=item.description)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)