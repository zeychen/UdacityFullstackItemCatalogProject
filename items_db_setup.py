import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# declarative_base() lets SQLAlchemy know that classes in file
# correspond to tables in db
Base = declarative_base()

############ Classes ###############
"""
Example mapper attributes:
	String(250)
	Integer
	relationship(Class)
	nullable = False (column must have a value in order for row to be created)
	primary_key = True
	ForeignKey('some_table.id')
"""


class Catagories(Base):

	__tablename__ = 'catagories'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)


class Items(Base):

	__tablename__ = 'item_catagory'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('catagories.id'))
	restaurant = relationship(Restaurant)


############ Ending Configuration ###############
engine = create_engine('sqlite:///catagories.db')

# adds data as new tables in db
Base.metadata.create_all(engine)