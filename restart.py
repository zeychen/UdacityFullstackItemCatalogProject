import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import items_db_setup
from items_db_setup import Base, Categories, Items
import items_dictionary

# Create session and connect to DB
engine = create_engine('sqlite:///categories.db')
Base.metadata.drop_all(engine)

os.system('python items_db_setup.py')
os.system('python items_dictionary.py')