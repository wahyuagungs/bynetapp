from sqlalchemy import Column, String, Integer, Float, DateTime, Sequence, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class VariableAllocationTag(BaseModel, db.Model):
    __tablename__ = 'var_allocation_tag'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('var_allocation_tag_id_seq'), primary_key=True, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('var_alloc_id', 'tag_id', name='unique_var_alloc_tag'),
    )

    var_alloc_id = Column(Integer, ForeignKey('variable_allocation.id'))
    tag_id = Column(Integer, ForeignKey('tag.id'))

