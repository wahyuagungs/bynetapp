from sqlalchemy import Column, String, Integer, Float, DateTime, Sequence, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class ElicitedProb(BaseModel, db.Model):
    __tablename__ = 'elicited_prob'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('elicited_prob_id_seq'), primary_key=True, nullable=False)
    value = Column(Float)

    # References
    var_alloc_id = Column(Integer, ForeignKey('variable_allocation.id'))
    probability_id = Column(Integer, ForeignKey('probability.id'))

    variable_allocation = relationship('VariableAllocation', foreign_keys='ElicitedProb.var_alloc_id')
    probability = relationship('Probability', foreign_keys='ElicitedProb.probability_id')
