from sqlalchemy import Column, String, Integer, Numeric, DateTime, Sequence, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel
from datetime import datetime


class Stage(BaseModel, db.Model):
    __tablename__ = 'stage'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('stage_id_seq'), primary_key=True, nullable=False)
    has_completed = Column(Boolean, default=False)
    start = Column(DateTime)
    end = Column(DateTime)

    # References
    ref_stage_id = Column(Integer, ForeignKey('ref_stage.id'))
    model_id = Column(Integer, ForeignKey('model.id'))
    user_id = Column(Integer, ForeignKey('app_user.id'))

    # Object References
    ref_stage = relationship('RefStage', foreign_keys='Stage.ref_stage_id')
    model = relationship('Model', foreign_keys='Stage.model_id')
    app_user = relationship('AppUser', foreign_keys='Stage.user_id')

    variable_allocations = relationship('VariableAllocation')
    weights = relationship('Weight')

    # def as_dict():
    #      result = {}
    #     for c in self.__table__.columns:
    #         if getattr(self, c.name) is None or isinstance(getattr(self, c.name),int):
    #             result[c.name] = getattr(self, c.name)
    #         else:
    #             result[c.name] = str(getattr(self, c.name))

    #     result['variable_allocations'] = []
    #     for va in self.variable_allocations:
    #         result['variable_allocations'].append(va.as_dict())

    #     return result
