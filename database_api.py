import os

from sqlalchemy import create_engine
from models.links import Base
from database.connections import load_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

engine = create_engine(f"sqlite:///{db_path}", echo=True)
Base.metadata.create_all(engine)
load_data()





