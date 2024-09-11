import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy_utils import database_exists, create_database
import config
from models import books

def url_parameters():
    load_dotenv()
    url = URL.create(
        drivername="postgresql",
        username=os.getenv("DB_LOGIN"),
        password=os.getenv("DB_PASSWORD"),
        database=config.DATABASE
    )
    return url

engine = create_engine(url_parameters(), echo=True)

def init_db():
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        engine.connect()
    books.Base.metadata.create_all(bind=engine)

def load_books_into_db(df):
    df.to_sql('books', con=engine, if_exists='replace', index_label="id")
