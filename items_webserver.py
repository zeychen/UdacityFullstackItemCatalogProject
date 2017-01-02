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





if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)