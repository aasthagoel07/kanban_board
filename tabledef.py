from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///kanban.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    def __init__(self, username, password):
        self.username = username
        self.password = password
 

class Task(Base):
    __tablename__="tasks"
    t_id=Column(Integer,primary_key=True)
    u_id=Column(Integer, ForeignKey("users.id"), nullable=False)
    task_name=Column(String)
    task_desc=Column(String)
    status = Column(String, default="Todo")
    def __init__(self ,u_id,task_name,task_desc,status):
        self.u_id=u_id
        self.task_name=task_name
        self.task_desc=task_desc
        self.status = status

# create tables
Base.metadata.create_all(engine)

# Task.__table__.drop(engine)