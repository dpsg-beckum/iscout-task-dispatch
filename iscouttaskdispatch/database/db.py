from __future__ import annotations

from typing import List, Type, TypeVar

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from .exceptions import ElementAlreadyExists, ElementDoesNotExsist

db = SQLAlchemy()

T = TypeVar('T', bound='BaseTable')


class BaseTable(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get_via_id(cls: Type[T], id: int) -> T:
        item = cls.query.get(id)
        if not item:
            raise ElementDoesNotExsist(
                f"{str(cls.__name__)} mit der ID \"{id}\" existiert nicht")
        return item

    @classmethod
    def get_all(cls: Type[T]) -> List[T]:
        return cls.query.all()

    def to_dict(self) -> dict:
        """
        Returns a dictionary with all parameters for calculation
        """
        data = {key: getattr(self, key)
                for key in self.__table__.columns.keys()}
        return data

    def save(self):
        db.session.commit()


class Status(BaseTable):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    tasks: Mapped[List[Task]] = relationship('Task', backref='status')

    @staticmethod
    def create_new(id, name):
        status = Status(id=id, name=name)
        db.session.add(status)
        db.session.commit()
        return status


class Team(BaseTable):
    __tablename__ = 'team'
    name = Column(String(255))
    description = Column(Text)

    tasks: Mapped[List[Task]] = relationship('Task', backref='team')

    def change_data(self, name: None | str = None, description: None | str = None):
        self.name = name if name else self.name
        self.description = description if description else self.description
        db.session.commit()
        return self

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['tasks'] = [task.to_dict() for task in self.tasks]

    @staticmethod
    def create_new(name, description):
        team = Team(name=name, description=description)
        db.session.add(team)
        db.session.commit()
        return team


class Task(BaseTable):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255))
    description = Column(Text)
    comment = Column(Text)
    team_id = Column(Integer, ForeignKey('team.id'))
    status_id = Column(Integer, ForeignKey('status.id'))

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['team'] = BaseTable.to_dict(Team.get_via_id(self.team_id))
        data['status'] = Status.get_via_id(self.status_id)
        return data

    @staticmethod
    def create_new(id, name="", description="", comment=""):
        try:
            Task.get_via_id(id)
            raise ElementAlreadyExists(
                f"Task mit der ID \"{id}\" existiert bereits")
        except ElementDoesNotExsist:
            pass

        task = Task(id=id,
                    name=name,
                    description=description,
                    comment=comment,
                    status_id=1)
        db.session.add(task)
        db.session.commit()
        return task
