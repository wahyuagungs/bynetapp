from sqlalchemy import Column, String, Integer, Float, Date, Sequence, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class Probability(BaseModel, db.Model):
    __tablename__ = 'probability'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('probability_id_seq'), primary_key=True, nullable=False)
    value = Column(Float, default=None)
    state_id = Column(Integer, ForeignKey('state.id'))

    probability_states = relationship("ProbabilityState", backref='Probability', lazy='dynamic')
    state = relationship('State', foreign_keys='Probability.state_id')
