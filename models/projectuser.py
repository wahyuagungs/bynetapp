from sqlalchemy import Column, Integer, Date, DateTime, String, Boolean, Sequence, ForeignKey
from models.base import db
from models.base_model import BaseModel
from sqlalchemy.orm import relationship


class ProjectUser(BaseModel, db.Model):
    __tablename__ = 'project_user'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('project_user_id_seq'), primary_key=True, nullable=False)

    #
    # Reference for the project
    #
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)

    #
    # Reference for the user
    #
    user_id = Column(Integer, ForeignKey('app_user.id'), nullable=False)

    project = relationship('Project', foreign_keys='ProjectUser.project_id')
    app_user = relationship('AppUser', foreign_keys='ProjectUser.user_id')
