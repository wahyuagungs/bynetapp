from sqlalchemy import Column, String, Integer, Numeric, Date, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from models.base import db
from models.base_model import BaseModel


class RefRole(BaseModel, db.Model):
    __tablename__ = 'ref_role'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('ref_role_id_seq'), primary_key=True, nullable=False)
    rolename = Column(String(100))
    role_description = Column(String(200))

    appuser_roles = relationship("AppUserRole")
    menu_roles = relationship('MenuRole')

