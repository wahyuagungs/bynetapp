from sqlalchemy import Column, String, Integer, Numeric, Date, Sequence, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class RefStage(BaseModel, db.Model):
    __tablename__ = 'ref_stage'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('ref_stage_id_seq'), primary_key=True, nullable=False)
    stage_label = Column(String(100))

    stages = relationship('Stage')
