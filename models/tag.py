from sqlalchemy import Column, String, Integer, Float, DateTime, Sequence, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class Tag(BaseModel, db.Model):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('tag_id_seq'), primary_key=True, nullable=False)
    label = Column(String(200), default=None)
    description = Column(Text, default=None)

    # references
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship('Model', foreign_keys='Tag.model_id')