from datetime import datetime
from sqlalchemy import Column, String, Integer, Numeric, Date, Sequence, ForeignKey, Text
from models.base import db
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Variable(BaseModel, db.Model):
    __tablename__ = 'variable'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('variable_id_seq'), primary_key=True, nullable=False)
    label = Column(String(100))
    description = Column(Text)
    model_id = Column(Integer, ForeignKey('model.id'))
    last_modified_by = Column(Integer, ForeignKey('app_user.id'))
    last_modified_date = Column(Date, default=None)
    created_by = Column(Integer, ForeignKey('app_user.id'))
    creation_date = Column(Date, default=datetime.now())

    # arcs_childs = relationship("Arc", backref='childs_var', lazy='dynamic', foreign_keys='Arc.child_id')
    # arcs_parents = relationship("Arc", backref='parents_var', lazy='dynamic', foreign_keys='Arc.parent_id')
    states = relationship("State", backref='Variable', lazy='dynamic')
    var_allocations = relationship("VariableAllocation")

    def get_states(self):
        # 'id': state.id, 'state_label': state.label
        output = []
        for state in self.states:
            output.append({'state_id': state.id, 'state_label': state.label})
        return output
