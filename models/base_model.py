from models.base import db
from sqlalchemy.sql import text


class BaseModel:

    def as_dict(self):
        result = {}
        for c in self.__table__.columns:
            if getattr(self, c.name) is None or isinstance(getattr(self, c.name),int):
                result[c.name] = getattr(self, c.name)
            else:
                result[c.name] = str(getattr(self, c.name))
        return result

    def update(self, quark):
        for key, value in quark.items():
            if value == 'False':
                setattr(self, key, False)
            elif value == 'True':
                setattr(self, key, True)
            elif value == 'None':
                setattr(self, key, None)
            elif value == "":
                setattr(self, key, None)
            else:
                setattr(self, key, value)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def save_all(args):
        for obj in args:
            db.session.add(obj)
        db.session.commit()

    def as_query(self):
        q = {}
        for c in self.__table__.columns:
            attr = getattr(self, c.name)
            if attr is not None:
                q[c.name] = attr
        return q

    @classmethod
    def get_list(cls, statement=None):
        if statement is None:
            return cls.query.all()
        else:
            return cls.query.filter_by(**statement.as_query()).all()

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __str__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())

