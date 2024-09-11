from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
import config

Base = declarative_base()

class Book(Base):
    __tablename__ = config.BOOKS_TABLE

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    page_count = Column(Integer)
    currently_reading_count = Column(Float)
    wanting_to_read_count = Column(Float)
    average_rating = Column(Float)
    amount_rating = Column(Integer)
    publishing_year = Column(Integer)
