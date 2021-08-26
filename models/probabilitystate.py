from sqlalchemy import Column, String, Integer, Numeric, Date, Sequence, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class ProbabilityState(BaseModel, db.Model):
    __tablename__ = 'probability_state'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('probability_state_id_seq'), primary_key=True, nullable=False)
    probability_id = Column(Integer, ForeignKey('probability.id'))
    state_id = Column(Integer, ForeignKey('state.id'))

    probability = relationship("Probability", foreign_keys='ProbabilityState.probability_id')
    state = relationship("State", foreign_keys='ProbabilityState.state_id')
