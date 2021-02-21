from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction

from .db_instance import db

from dotenv import load_dotenv
load_dotenv()

import os

Base = declarative_base()

engine = create_engine(os.getenv("DB_CONN"), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

modesOfTransportation = [
  {
    "code": "dieselCar", 
    "name": "Diesel Car"
  },
  {
    "code": "petrolCar",
    "name": "Petroleum Car"
  },
  {
    "code": "anyCar",
    "name": "Other Car" 
  },
  {
    "code": "taxi",
    "name": "Taxi" 
  },
  {
    "code": "economyFlight",
    "name": "Economy Flight" 
  },
  {
    "code": "businessFlight",
    "name": "Business Flight"
  },
  {
    "code": "firstclassFlight",
    "name": "First-Class Flight"
  },
  {
    "code": "motorbike",
    "name": "Motorcycle"
  },
  {
    "code": "bus",
    "name": "Bus"
  },
  {
    "code": "transitRail",
    "name": "Metro"
  }
]

class ModeOfTransportation(db.Model):  # Base
    __tablename__ = 'transportation'
    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    
def add_all_mode_of_trans():
    allModesOfTrans = []
    for idx, modeOfTransportation in enumerate(modesOfTransportation):
        allModesOfTrans.append(
            ModeOfTransportation(id=idx, code=modeOfTransportation['code'], name=modeOfTransportation['name'])
        )
    session.add_all(allModesOfTrans)
    session.commit()

def get_all_mode_of_trans():
    return session.query(ModeOfTransportation).all()

# add_all_mode_of_trans()
# run_transaction(sessionmaker(bind=engine), ModeOfTransportation.query().delete())  # delete old data
# run_transaction(sessionmaker(bind=engine), add_all_mode_of_trans)    # add new data
