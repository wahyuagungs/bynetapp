from sqlalchemy import Column, String, Integer, Numeric, DateTime, Sequence, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class CPCState(BaseModel, db.Model):
    __tablename__ = 'cpc_state'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('cpc_state_id_seq'), primary_key=True, nullable=False)

    # Object References
    state = relationship('State', foreign_keys='CPCState.state_id')
    cpc = relationship('CPC', foreign_keys='CPCState.cpc_id')

    # References
    state_id = Column(Integer, ForeignKey('state.id'))
    cpc_id = Column(Integer, ForeignKey('cpc.id'))
    parent_id = Column(Integer, ForeignKey('cpc_state.id'))

