from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime

db = SQLAlchemy()

class Status(db.Model):
    __tablename__ = 'Status'
    statusID = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(255))

class Team(db.Model):
    __tablename__ = 'Team'
    teamID = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(255))

class Task(db.Model):
    __tablename__ = 'Task'
    taskID = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(255))
    description = Column(Text)
    teamID = Column(Integer, ForeignKey('Team.teamID'))

class TaskHasStatus(db.Model):
    __tablename__ = 'TaskHasStatus'
    taskstatusID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    taskID = Column(Integer, ForeignKey('Task.taskID'), nullable=False)
    statusID = Column(Integer, ForeignKey('Status.statusID'), nullable=False)
    timestamp = Column(DateTime)

def seed_status_table():
    # Assuming that the Status table is empty
    statuses = [
        {"statusID": 1, "name": "Created"},
        {"statusID": 2, "name": "Assigned"},
        {"statusID": 3, "name": "Work in Progress"},
        {"statusID": 4, "name": "Done"},
        {"statusID": 5, "name": "Failed"}
    ]

    for status_data in statuses:
        status = Status(**status_data)
        db.session.add(status)

    db.session.commit()