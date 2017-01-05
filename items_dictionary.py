from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from items_db_setup import Base, Categories, Items, User

# Create session and connect to DB
engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# categories and items for testing purposes

user1 = User(name="zeechen", email="icecreamcapucino@gmail.com")
session.add(user1)
session.commit()

user2 = User(name="chen", email="test@test.com")
session.add(user2)
session.commit()

category1 = Categories(name = "sports", user_id=1)
session.add(category1)
session.commit()

cat1item1 = Items(name="tennis", description="tennis description", category=category1, user_id=1)
session.add(cat1item1)
session.commit()

cat1item2 = Items(name="soccer", description="soccer description", category=category1, user_id=1)
session.add(cat1item2)
session.commit()

cat1item3 = Items(name="frisbee", description="frisbee description", category=category1, user_id=2)
session.add(cat1item3)
session.commit()

category2 = Categories(name = "movies", user_id=1)
session.add(category2)
session.commit()

cat2item1 = Items(name="Secret Life of Pets", description="Secret Life of Pets description", category=category2, user_id=1)
session.add(cat2item1)
session.commit()

category3 = Categories(name = "TV shows", user_id=1)
session.add(category3)
session.commit()

cat3item1 = Items(name="criminal minds", description="criminal minds description", category=category3, user_id=2)
session.add(cat3item1)
session.commit()

category4 = Categories(name = "holidays", user_id=2)
session.add(category4)
session.commit()

cat4item1 = Items(name="christmas", description="christmas description", category=category4, user_id=1)
session.add(cat4item1)
session.commit()

print "added items!"