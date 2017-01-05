import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from items_db_setup import Base, Categories, Items, User


# Create session and connect to DB
engine = create_engine('sqlite:///categories.db')
Base.metadata.drop_all(engine)

# import items_db_setup
# import items_dictionary
os.system('python items_db_setup.py')
print "db setup complete"
os.system('python items_dictionary.py')
print "import data complete"