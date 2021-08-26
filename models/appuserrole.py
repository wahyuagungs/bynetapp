from sqlalchemy import Column, Integer, Sequence, ForeignKey
from models.base import db
from models.base_model import BaseModel


class AppUserRole(BaseModel, db.Model):
    __tablename__ = 'app_user_role'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('app_user_role_id_seq'), primary_key=True, nullable=False)

    #
    # Reference for the user
    #
    app_user = Column(Integer, ForeignKey('app_user.id'),nullable=False)

    #
    # Reference for the role
    #
    ref_role = Column(Integer, ForeignKey('ref_role.id'), nullable=False)

    # def __init__(self, app_user, ref_role):
    #     self.app_user = app_user
    #     self.ref_role = ref_role
