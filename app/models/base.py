import datetime
from contextlib import contextmanager

from flask_sqlalchemy import BaseQuery
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import asc, desc


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


db = SQLAlchemy(query_class=BaseQuery)


class Base(db.Model):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def create(cls, **kwargs):
        base = cls()
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(cls, key):
                        setattr(base, key, value)
            if hasattr(cls, 'create_time'):
                setattr(base, 'create_time', datetime.datetime.now())
            db.session.add(base)
        return base

    def modify(self, **kwargs):
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(self, key):
                        setattr(self, key, value)

    def delete(self):
        with db.auto_commit():
            db.session.delete(self)

    @classmethod
    def search(cls, **kwargs):
        db.session.commit()
        res = cls.query
        for key, value in kwargs.items():
            if value is not None:
                if hasattr(cls, key):
                    if isinstance(value, str):
                        res = res.filter(getattr(cls, key).like('%' + value + '%'))
                    else:
                        res = res.filter(getattr(cls, key) == value)

        if kwargs.get('order'):
            for key, value in kwargs['order'].items():
                if hasattr(cls, key):
                    if value == 'asc':
                        res = res.order_by(asc(getattr(cls, key)))
                    elif value == 'desc':
                        res = res.order_by(desc(getattr(cls, key)))
        page = kwargs.get('page') if kwargs.get('page') else 1
        page_size = kwargs.get('page_size') if kwargs.get('page_size') else 20
        data = {
            'meta': {
                'count': res.count(),
                'page': page,
                'page_size': page_size
            }
        }

        res = res.offset((page - 1) * page_size).limit(page_size)
        res = res.all()
        data['data'] = res
        return data
