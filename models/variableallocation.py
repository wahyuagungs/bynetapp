from sqlalchemy import Column, String, Integer, Numeric, DateTime, Sequence, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel
from datetime import datetime


class VariableAllocation(BaseModel, db.Model):
    __tablename__ = 'variable_allocation'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('variable_allocation_id_seq'), primary_key=True, nullable=False)
    has_completed = Column(Boolean, default=False)

    # References
    variable_id = Column(Integer, ForeignKey('variable.id'))
    stage_id = Column(Integer, ForeignKey('stage.id'))

    # many-to-one references
    variable = relationship('Variable', foreign_keys='VariableAllocation.variable_id')
    stage = relationship('Stage', foreign_keys='VariableAllocation.stage_id')

    # one-to-many references
    elicited_probs = relationship("ElicitedProb")
    cpcs = relationship("CPC")
