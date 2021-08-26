from sqlalchemy import Column, Integer, Date, DateTime, String, Boolean, Sequence, Text
from models.base import db
from models.base_model import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship


class Project(BaseModel, db.Model):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('project_id_seq'), primary_key=True, nullable=False)
    title = Column(String(50))
    description = Column(Text)
    max_participants = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    is_activated = Column(Boolean, default=False)
    last_modified_date = Column(DateTime)
    creation_date = Column(DateTime, default=datetime.now())

    project_users = relationship("ProjectUser", backref='Project', lazy='dynamic')
    models = relationship("Model", backref='Project', lazy='dynamic')