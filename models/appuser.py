from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, DateTime, Sequence, Boolean, Text
from sqlalchemy.orm import relationship, synonym
from models.base import db
from models.base_model import BaseModel
from passlib.hash import pbkdf2_sha256


class AppUser(BaseModel, db.Model):
    __tablename__ = 'app_user'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, Sequence('app_user_id_seq'), primary_key=True, nullable=False)
    firstname = Column(String(200), nullable=False)
    lastname = Column(String(200))
    email = Column(String(200), nullable=False, unique=True)
    phone = Column(String(50), nullable=True)
    organisation = Column(String(200))
    is_activated = Column(Boolean, default=False)
    activation_date = Column(DateTime)
    username = Column(String(500), nullable=False, unique=True)
    _password_hash = Column('password', String(2000), nullable=False)
    enabled = Column(Boolean, default=True)
    consented_date = Column(Date)
    activation_token = Column(Text, nullable=False)
    creation_date = Column(DateTime, default=datetime.now())

    accesslogs = relationship("AccessLog")
    appuser_roles = relationship("AppUserRole", cascade="all,delete", backref='AppUser', lazy='dynamic')

    # appuser_roles = relationship(iter"AppUserRole")
    appuser_projects = relationship("AppUserRole")
    stages = relationship("Stage")

    @property
    def password(self):
        return None

    @password.setter
    def password(self, val):
        if val is not None:
            self._password_hash = pbkdf2_sha256.hash(val)

    password = synonym('_password_hash', descriptor=password)


    def verify(self, _password):
        return pbkdf2_sha256.verify(_password, self._password_hash)

    def as_dict(self):
        result = {}
        for c in self.__table__.columns:
            if getattr(self, c.name) is None or isinstance(getattr(self, c.name),int):
                result[c.name] = getattr(self, c.name)
            else:
                result[c.name] = str(getattr(self, c.name))

        result['roles'] = []
        for role in self.appuser_roles:
            result['roles'].append(role.as_dict())

        return result


