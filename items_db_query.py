# import database functions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from items_db_setup import Base, Categories, Items

# Create session and connect to DB
engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


def db_categories(db_session):
	"""
	List all catgories in database sorted alphabetically
	"""
	categories = db_session.query(Categories).order_by(Categories.name).all()
	return categories


def db_category(db_session, category_id):
	"""
	List specific category id
	"""
	category = db_session.query(Categories).filter_by(id=category_id).one()
	return category


def db_items(db_session, category_id):
	"""
	List all items in specified category
	"""
	items = db_session.query(Items).filter_by(category_id=category_id).order_by(Items.name).all()
	return items


def db_item(db_session, item_id):
	"""
	List specific item in specified category
	"""
	item = db_session.query(Items).filter_by(id=item_id).one()
	return item

