import sys
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, BigInteger, JSON, DateTime
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(
    __file__), os.path.pardir, os.path.pardir, os.path.pardir)))
from hidden import DATABASE, USER, PASSWORD, HOST, PORT

Base = declarative_base()

class MeteoFrance(Base):
    __tablename__ = 'french_cities_weather'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    rain = Column(String)
    snow = Column(String)
    clouds = Column(Integer)
    wind = Column(String)
    weather_desc = Column(String)
    weather_icon = Column(String)
    readable_warnings = Column(String)

def connect_to_database():
    engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def create_table(session):
    Base.metadata.create_all(session.get_bind())
