from sqlalchemy import Column, String, Integer, Numeric, Date, Sequence, ForeignKey
from sqlalchemy.orm import relationship, synonym
from models.base import db
from models.base_model import BaseModel


class RefMenu(BaseModel, db.Model):
    __tablename__ = 'ref_menu'
    _id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    # _id = Column('id', Integer, Sequence('ref_menu_id_seq'), primary_key=True, nullable=False)
    _link = Column('link', String(200))
    _title = Column('title', String(200))
    _class_picture = Column('class_picture', String(50))
    _parent_id = Column('parent_id', Integer, ForeignKey('ref_menu.id'))

    menu_roles = relationship('MenuRole')

    def __init__(self, _link, _title, _class_picture, _parent_id=None, _childItems=None):
        self._link = _link
        self._title = _title
        self._class_picture = _class_picture
        self._parent_id = _parent_id
        self._childItems = _childItems

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    id = synonym('_id', descriptor=id)

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, val):
        self._link = val

    link = synonym('_link', descriptor=link)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    title = synonym('_title', descriptor=title)

    @property
    def class_picture(self):
        return self._class_picture

    @class_picture.setter
    def class_picture(self, val):
        self._class_picture = val

    class_picture = synonym('_class_picture', descriptor=class_picture)

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, val):
        self._parent_id = val

    parent_id = synonym('_parent_id', descriptor=parent_id)

    @property
    def childItems(self):
        return self._childItems

    @childItems.setter
    def childItems(self, val):
        self._childItems = val

    def append(self, obj):
        if self._childItems is None:
            self._childItems = []
            self._childItems.append(obj)
        else:
            self._childItems.append(obj)

    def as_dict(self):
        out = {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
        if hasattr(self, 'childItems'):
            out['childItems'] = []
            for item in self.childItems:
                out['childItems'].append(item.as_dict())
            return out
        else:
            return out
