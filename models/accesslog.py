from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Sequence, Boolean, ForeignKey, Text
from models.base import db
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class AccessLog(BaseModel, db.Model):
    __tablename__ = 'access_log'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('access_log_id_seq'), primary_key=True, nullable=False)
    ip_address = Column(String(50))
    browser_agent = Column(Text)
    activity_type = Column(Integer, default=0) # 0: not important, 1: Important, 2: private detail
    activity = Column(Text)
    creation_date = Column(DateTime, default=datetime.now())
    #
    # Reference for the User
    #
    user = Column(Integer, ForeignKey('app_user.id'))

    app_user = relationship("AppUser", foreign_keys='AccessLog.user')
