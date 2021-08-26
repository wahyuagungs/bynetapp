from sqlalchemy import Column, String, Integer, Float, DateTime, Sequence, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class CPC(BaseModel, db.Model):
    __tablename__ = 'cpc'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('cpc_id_seq'), primary_key=True, nullable=False)
    is_completed = Column(Boolean, default=False)

    # Object References
    variable_allocation = relationship('VariableAllocation', foreign_keys='CPC.var_alloc_id')
    variable = relationship('Variable', foreign_keys='CPC.base_variable_id')

    cpc_states = relationship('CPCState')

    # References
    base_variable_id = Column(Integer, ForeignKey('variable.id'))
    user_id = Column(Integer, ForeignKey('app_user.id'))
    var_alloc_id = Column(Integer, ForeignKey('variable_allocation.id'))

