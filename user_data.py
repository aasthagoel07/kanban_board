import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
 
engine = create_engine('sqlite:///kanban.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User(username="admin",password="password")
session.add(user)
 
user = User(username="aastha",password="aastha1234")
session.add(user)
 
user = User(username="user",password="abcd")
session.add(user)
 
# commit the record the database
session.commit()

session.commit()