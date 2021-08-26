from sqlalchemy import Column, String, Integer, Float, DateTime, Sequence, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class Weight(BaseModel, db.Model):
    __tablename__ = 'weight'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('weight_id_seq'), primary_key=True, nullable=False)
    value = Column(Float)
    has_completed = Column(Boolean, default=False)

    # Object References
    variable = relationship('Variable', foreign_keys='Weight.variable_id')
    parent_variable = relationship('Variable', foreign_keys='Weight.parent_variable_id')
    stage = relationship('Stage', foreign_keys='Weight.stage_id')

    # References
    variable_id = Column(Integer, ForeignKey('variable.id'))
    user_id = Column(Integer, ForeignKey('app_user.id'))
    parent_variable_id = Column(Integer, ForeignKey('variable.id'))
    stage_id = Column(Integer, ForeignKey('stage.id'))

