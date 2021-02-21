from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction

from dotenv import load_dotenv
load_dotenv()

import os

Base = declarative_base()

engine = create_engine(os.getenv("DB_CONN"), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

actions = [
  {
    "name": "planting a tree",
    "kgSavePerYear": 31
  },
  {
    "name": "air drying laundry",
    "kgSavePerYear": 153
  },
  {
    "name": "turning down thermostat by 10 degrees Fahrenheit",
    "kgSavePerYear": 184
  },
  {
    "name": "taking shorter showers",
    "kgSavePerYear": 23
  },
  {
    "name": "turning off electrical equiment when not in use",
    "kgSavePerYear": 5
  },
]

class Action(Base):
    __tablename__ = 'action'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    kgsaveperyear = Column(Integer)

def add_all_actions():
    allActions = []
    for idx, action in enumerate(actions):
        allActions.append(
            Action(id=(idx * 10 + 20), name=action['name'], kgsaveperyear=action['kgSavePerYear'])  # multiply id to avoid collision with other tables
        )
    session.add_all(allActions)
    session.commit()

def get_all_actions():
    return session.query(Action).all()

# add_all_actions()

# run_transaction(sessionmaker(bind=engine), Action.query().delete())  # delete old data
# run_transaction(sessionmaker(bind=engine), add_all_actions)  # add new data
