import uuid
from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.state import InstanceState
from sqlalchemy import Column, String, SmallInteger, Boolean, CheckConstraint, ForeignKey, DateTime, Index


db = SQLAlchemy(app)
Base = declarative_base()


def get_dict(self):
    result = dict(self.__dict__)
    items_to_remove = []
    for item in result:
        if isinstance(result[item], InstanceState):
            items_to_remove.append(item)
    for item in items_to_remove:
        del result[item]
    return result


Base.get_dict = get_dict


class Employee(Base):
    __tablename__ = 'employees'


