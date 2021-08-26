from sqlalchemy import Column, Integer, Date, DateTime, String, Boolean, Sequence, ForeignKey, Text
from models.base import db
from models.base_model import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship


class Model(BaseModel, db.Model):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('project_id_seq'), primary_key=True, nullable=False)
    version = Column(String(10))
    data_content = Column(Text)
    has_loaded = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    total_variables = Column(Integer)
    creation_date = Column(DateTime, default=datetime.now())

    #
    # Reference for the project
    #
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    project = relationship('Project', foreign_keys='Model.project_id')
    variables = relationship('Variable')
    stages = relationship('Stage')


