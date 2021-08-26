from sqlalchemy import Column, String, Integer, Numeric, Date, Sequence, Text
from models.base import db
from models.base_model import BaseModel


class AppProfile(BaseModel, db.Model):
    __tablename__ = 'app_profile'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('app_profile_id_seq'), primary_key=True, nullable=False)
    information = Column(Text)
    organisation = Column(String(200))
    email = Column(String(50))
    url = Column(String(255))
    title = Column(String(255))


