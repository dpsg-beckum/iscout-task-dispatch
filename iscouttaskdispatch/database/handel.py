from . import db
from .json_encoder import DatabaseEncoder
from .db import Team, Task, TaskHasStatus, Status
from datetime import datetime as dt
from .exceptions import *

def setTaskName(taskID: int, name: str):
    task : Task = Task.query.get(taskID)
    task.name = name
    db.session.commit()

def setTaskDescription(taskID: int, description: str):
    task : Task = Task.query.get(taskID)
    task.description = description
    db.session.commit()

def getAllTasks():
    return [DatabaseEncoder.default(i) for i in Task.query.all()]

def getTaskViaID(taskID : int):
    return DatabaseEncoder.default(Task.query.get(taskID))

def createTask(taskID:int, name:str, description: str):
    if not Task.query.get(taskID):
        db.session.add(Task(taskID = taskID, name=name, description=description))
        db.session.commit()
        return DatabaseEncoder.default(Task.query.get(taskID))
    else:
        raise ElementAlreadyExists()

def deleteTask(taskID: int):
    if Task.query.get(taskID):
        db.session.delete(db.session.query(Task).get(taskID))
        db.session.commit()
    else:
        raise ElementDoesNotExsist()

def getAllTeams():
    return [DatabaseEncoder.default(i) for i in Team.query.all()]

def getTeamViaID(teamID:int):
    return DatabaseEncoder.default(Team.query.get(teamID))

def createTeam(teamID:int, name: str):
    if not Team.query.get(teamID):
        db.session.add(Team(teamID = teamID, name=name))
        db.session.commit()
        return DatabaseEncoder.default(Team.query.get(teamID))
    else:
        raise ElementAlreadyExists()

def deleteTeam(teamID:int):
    if Team.query.get(teamID):
            x = db.session.query(Team).get(teamID)
            db.session.delete(x)
            db.session.commit()
    else:
        raise ElementDoesNotExsist()

def setTaskStatus(taskID: int, statusID: int):
    db.session.add(TaskHasStatus(taskID=taskID, statusID=statusID, timestamp=dt.now()))
    db.session.commit()
    pass

def assignTask(taskID: int, teamID: int):
    task : Task = Task.query.get(taskID)
    task.teamID = teamID
    db.session.commit()
    setTaskStatus(taskID, 2)

