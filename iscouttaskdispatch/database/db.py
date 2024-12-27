from __future__ import annotations

from datetime import datetime
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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
    name = Column(String(255))

    tasks: Mapped[List[Task]] = relationship('Task', back_populates='status')

    def to_dict(self) -> dict:
        data = super().to_dict()
        colors = ['secondary', 'primary',
                  'success', 'danger']
        data.update({'html_color': colors[self.id-1]})
        return data

    def delete(self):
        raise Exception("Status kann nicht gelöscht werden")

    @staticmethod
    def create_new(id, name):
        status = Status(id=id, name=name)
        db.session.add(status)
        db.session.commit()
        return status


class Team(BaseTable):
    __tablename__ = 'team'
    name = Column(String(255))
    tasks: Mapped[List[Task]] = relationship('Task', back_populates='team')

    def change_data(self, name: None | str = None, description: None | str = None):
        self.name = name if name else self.name
        self.description = description if description else self.description
        db.session.commit()
        return self

    def to_dict(self, prevent_recursion=False) -> dict:
        data = super().to_dict()
        if not prevent_recursion:
            data['tasks'] = [task.to_dict(True) for task in self.tasks]
        return data

    @staticmethod
    def create_new(name, check_exists=True):
        if check_exists:
            alredyexisting = Team.query.filter_by(name=name).all()
            if alredyexisting:
                raise ElementAlreadyExists(
                    f"Team mit dem Namen \"{name}\" ({alredyexisting}) existiert bereits")

        team = Team(name=name)
        db.session.add(team)
        db.session.commit()
        return team


class Task(BaseTable):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255))
    description = Column(Text)
    format = Column(Text)
    link = Column(Text)
    comment = Column(Text)
    log = Column(Text, default="")
    team_id = Column(Integer, ForeignKey('team.id'), nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False)

    team: Mapped[Team] = relationship(
        'Team', back_populates='tasks')
    status: Mapped[Status] = relationship(
        'Status', back_populates='tasks')

    def to_dict(self, prevent_recursion=False) -> dict:
        data = super().to_dict()
        if not prevent_recursion:
            data['team'] = self.team.to_dict(True) if self.team else None
        data['status'] = self.status.to_dict() if self.status else None
        return data

    def update_data(self, name: None | str = None, description: None | str = None, comment: None | str = None, link: None | str = None, format: None | str = None, status_id: None | int = None, updated_by: str = "Unbekannt"):
        logs = []

        if name and name != self.name:
            logs.append("Name")
            self.name = name.strip()

        if description and description != self.description:
            logs.append("Beschreibung")
            self.description = description.strip()

        if comment and comment != self.comment:
            logs.append("Kommentar")
            self.comment = comment.strip()

        if link and link != self.link:
            logs.append("Link")
            self.link = link.strip()

        if format and format != self.format:
            logs.append("Format")
            self.format = format.strip()

        if status_id:
            status_id = int(status_id)
            status = Status.get_via_id(status_id)
            if status_id != self.status_id:
                print(status_id, self.status_id)
                logs.append(f"Status geändert auf \
                            {status.name}")
                self.status_id = status.id

        if logs:
            self._write_log(f"Task aktualisiert durch \
                            {updated_by} mit: {', '.join(logs)}")

        db.session.commit()
        return self

    @staticmethod
    def create_new(id, name="", description="", comment="", link="", format=""):
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
                    link=link,
                    format=format,
                    status_id=1)
        db.session.add(task)
        task._write_log("Task erstellt")
        db.session.commit()
        return task

    def _write_log(self, log: str):
        if self.log is None:
            self.log = ""
        self.log += datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
            " " + log.strip() + "\n"

    def set_status(self, status_id, log=f"Status geändert auf {status_id}"):
        self.status_id = status_id
        self._write_log(log)
        db.session.commit()
        return self

    def get_unassigned_tasks() -> List[Task]:
        return Task.query.filter(Task.team_id == None).all()

    def assign_to_team(self, team: Team, overwrite=False):
        if (not overwrite) and (self.team_id and self.team_id != team.id):
            raise Exception(
                f"Task ist bereits zugewiesen an Team {self.team_id}")
        self.team_id = team.id
        self.status_id = 2
        log = f"Task zugewiesen an {team.name}"
        if overwrite:
            log += f" (Überschrieben)"
        self._write_log(log)
        db.session.commit()
        return self
