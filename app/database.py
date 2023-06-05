from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# loading env variable
load_dotenv()


db_url = f"postgresql://{os.environ.get('SQL_USERNAME')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}/{os.environ.get('SQL_DBNAME')}"
engine = create_engine(
    url = db_url
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()