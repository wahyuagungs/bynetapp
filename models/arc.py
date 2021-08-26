from datetime import datetime
from sqlalchemy import Column, String, Integer, Numeric, Date, Sequence, ForeignKey
from models.base import db
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Arc(BaseModel, db.Model):
    __tablename__ = 'arc'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('arc_id_seq'), primary_key=True, nullable=False)
    parent_id = Column(Integer, ForeignKey('variable.id'))
    child_id = Column(Integer, ForeignKey('variable.id'))

    parent = relationship("Variable", foreign_keys='Arc.parent_id')
    child = relationship("Variable", foreign_keys='Arc.child_id')
