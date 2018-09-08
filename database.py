# coding: utf-8
from sqlalchemy import Column, Float, Integer, String, Text, text, create_engine
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata
engine = create_engine('sqlite:///trainsdb.db', echo=True)


class FromToSuggestion(Base):
    __tablename__ = 'from_to_suggestions'

    from_station = Column(String(10), primary_key=True)
    to_stations = Column(Text)


class StationAkaInfo(Base):
    __tablename__ = 'station_aka_info'

    station_code = Column(String(20), primary_key=True, nullable=False)
    title = Column(String(128), primary_key=True, nullable=False)
    pop = Column(Integer, server_default=text("0"))


class StationAkaInfoLocal(Base):
    __tablename__ = 'station_aka_info_local'

    station_code = Column(String(20), primary_key=True, nullable=False)
    title = Column(String(128), primary_key=True, nullable=False)


class StationInfo(Base):
    __tablename__ = 'station_info'

    station_code = Column(String(10), primary_key=True)
    title = Column(String(128))
    gid = Column(String(10))
    pop = Column(Integer)
    lat = Column(Float)
    lng = Column(Float)
    uber_available = Column(Integer, server_default=text("-1"))
    title_soundex = Column(String(128))
    title_soundex_index = Column(String(128))


class StationInfoLocal(Base):
    __tablename__ = 'station_info_local'

    title = Column(String(128))
    gid = Column(String(10), primary_key=True)


class TrainAkaInfo(Base):
    __tablename__ = 'train_aka_info'

    train_no = Column(String(10), primary_key=True, nullable=False)
    train_name = Column(String(128), primary_key=True, nullable=False)
    pop = Column(Integer)


class TrainAkaInfoLocal(Base):
    __tablename__ = 'train_aka_info_local'

    train_no = Column(String(10), primary_key=True, nullable=False)
    train_name = Column(String(128), primary_key=True, nullable=False)


class TrainInfo(Base):
    __tablename__ = 'train_info'

    train_no = Column(String(10), primary_key=True)
    train_name = Column(String(128))
    train_type = Column(String(128))
    title_soundex = Column(String(128))
    title_soundex_index = Column(String(128))
    classes = Column(Integer)
    pop = Column(Integer)


class TrainInfoLocal(Base):
    __tablename__ = 'train_info_local'

    train_no = Column(String(10), primary_key=True)
    train_name = Column(String(128))

session = create_session(bind=engine)