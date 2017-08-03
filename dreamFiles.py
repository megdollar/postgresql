from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import random
import calendar

from database_setup import Category, Item, Base, User

engine = create_engine('sqlite:///dreamswithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()\

session = DBSession()


# Create user
User1 = User(name="Megan Dollar", email="megdollar@gmail.com",
             picture='https://media.licdn.com/mpr/mpr/shrinknp_200_200/'
                     'AAEAAQAAAAAAAAmbAAAAJGJkZDhkMDA2LTlmNWQtNDU1My1i'
                     'YTE0LWJkOGRhYWEyOGIyYg.jpg')
session.add(User1)
session.commit()


def RandomDate(years=1):
    today = datetime.date.today()
    # Set the default dates
    day = today.day
    year = today.year
    month = today.month
    month = random.randint(1, month)
    day = random.randint(1, day - 1)

    return datetime.date(year, month, day)

# Add Recurring Dream category and item
category1 = Category(user_id=1, name="Recurring",
                     description="Repeating dreams are signs that we are not "
                     "paying attention to the message given.")

session.add(category1)
session.commit()

dream1 = Item(user_id=1, title="That Highschool Dream",
              description="Last night I had that dream about being stuck "
              "back in highschool, and not being able to graduate. I have "
              "had this dream many times before.", emotion="anxiety",
              dream_date=RandomDate(), category=category1)

session.add(dream1)
session.commit()

# Add Nightmare category and item
category2 = Category(user_id=1, name="Nightmare",
                     description="These are the most emotionally draining of "
                     "all dreams. They may represent issues in our waking "
                     "lives that the subconscious drives the sleeper to "
                     "acknowledge through fear.")

session.add(category2)
session.commit()

dream2 = Item(user_id=1, title="Teeth Falling out",
              description="While eating popcorn at a movie my teeth started "
              "to fall out and fill my popcorn bucket.", emotion="horror",
              dream_date=RandomDate(), category=category2)

session.add(dream2)
session.commit()

# Add Lucid category and item
category3 = Category(user_id=1, name="Lucid",
                     description="In these dreams the sleeper is actually "
                     "aware that they are in a dream state. The dream is "
                     "so vivid it seems real, although events and characters "
                     "will often be greatly exaggerated.")

session.add(category3)
session.commit()

dream3 = Item(user_id=1, title="Flying",
              description="During my dream about skydiving I became aware that"
              " I was dreaming and I was able to feel the rush of air around "
              "me and the palpitations in my chest as I soared through the "
              "air.", emotion="excitement", dream_date=RandomDate(),
              category=category3)

session.add(dream3)
session.commit()


# Add Daily life category and item
category4 = Category(user_id=1, name="Daily Life",
                     description="Dreams that incorporate familiar faces and"
                     " places do not necessarily reveal hidden symbolic "
                     "messages from the subconscious. They are simply "
                     "reflections of everyday life.")

session.add(category4)
session.commit()

dream4 = Item(user_id=1, title="Commute",
              description="I dreamt of my commute in to work last night, "
              "the traffic, and the usual podcasts I listen to enroute.",
              emotion="content", dream_date=RandomDate(), category=category4)

session.add(dream4)
session.commit()

# Add Physiological Category and item
category5 = Category(user_id=1, name="Physiological",
                     description="Some dreams are said to be direct "
                     "reflections of our needs in the conscious world. For "
                     "example, a dream where the sleeper is shivering in "
                     "the snow may simply mean an extra blanket is required.")

session.add(category5)
session.commit()

dream5 = Item(user_id=1, title="Jungle Adventures",
              description="I had a very vivid dream about exploring the swampy"
              " jungle last night. I woke up to find I was sweaty and hot!",
              emotion="discomfort", dream_date=RandomDate(),
              category=category5)

session.add(dream5)
session.commit()

# Add Problem Solving category and iem
category6 = Category(user_id=1, name="Problem Solving",
                     description="These dreams are designed to impart a "
                     "message to the sleeper that will aid them in "
                     "overcoming a problem in their conscious life.")

session.add(category6)
session.commit()

dream6 = Item(user_id=1, title="Calculations",
              description="In my dream I was trying to solve a complex "
              "algorithm. In my waking life I have been stuck on this problem"
              " for a while, but in this dream I was able to solve it. ",
              emotion="clear minded", dream_date=RandomDate(),
              category=category6)

session.add(dream6)
session.commit()


print "added dreams!"
