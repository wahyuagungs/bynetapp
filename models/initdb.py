from sqlalchemy import create_engine
from models.base import db


def construct_database(engine):
    db_engine = create_engine(engine, echo=True)
    db.Model.metadata.create_all(db_engine)
