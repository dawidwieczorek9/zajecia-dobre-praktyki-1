from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DB = "sqlite:///./auth.db"

engine = create_engine(DB, echo=True)
Base = declarative_base()
db = Session(bind=engine)