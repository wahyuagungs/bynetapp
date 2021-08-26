from sqlalchemy import Column, String, Integer, Date, Sequence, ForeignKey
from models.base import db
from models.base_model import BaseModel


class MenuRole(BaseModel, db.Model):
    __tablename__ = 'menu_role'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('menu_role_id_seq'), primary_key=True, nullable=False)

    #
    # Reference for the user
    #
    ref_menu = Column(Integer, ForeignKey('ref_menu.id'))

    #
    # Reference for the role
    #
    ref_role = Column(Integer, ForeignKey('ref_role.id'))

    def __init__(self, ref_menu, ref_role):
        self.ref_menu = ref_menu
        self.ref_role = ref_role
