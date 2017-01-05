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

class Users(Base):
	__tablename__ = 'user'

	id = Column(String(80), primary_key = True)
	name = Column(String(80))

	@property
	def serialize(self):
		"""
		returns object in serialized format
		"""
		return {
			'id': self.id,
			'name': self.name
		}

class Categories(Base):

	__tablename__ = 'category'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)

	@property
	def serialize(self):
		"""
		returns object in serialized format
		"""
		return {
			'name': self.name,
			'id': self.id,
		}
	

class Items(Base):

	__tablename__ = 'item'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))

	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship('Categories')
	
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship('Users')

	@property
	def serialize(self):
		"""
		returns object in serialized format
		"""
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'category_id': self.category_id,
			'user_id': self.user_id,
		}


############ Ending Configuration ###############
engine = create_engine('sqlite:///categories.db')

# adds data as new tables in db
Base.metadata.create_all(engine)