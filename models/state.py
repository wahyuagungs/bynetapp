from sqlalchemy import Column, String, Integer, Numeric, Date, Sequence, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class State(BaseModel, db.Model):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('state_id_seq'), primary_key=True, nullable=False)
    label = Column(String(100))
    description = Column(Text)
    variable_id = Column(Integer, ForeignKey('variable.id'))

    probabilities = relationship("Probability", backref='State', lazy='dynamic')
    probability_states = relationship("ProbabilityState", backref='State', lazy='dynamic')

    variable = relationship('Variable', foreign_keys='State.variable_id')
