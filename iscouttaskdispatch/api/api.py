from flask import Blueprint, request, Response, abort, jsonify
from ..database.db import db
from ..database.json_encoder import DatabaseEncoder
from ..database.db import Team, Task, TaskHasStatus, Status

api_routes = Blueprint("api", __name__, template_folder="templates",
                       url_prefix="")



@api_routes.route("/task", methods=['GET'])
def AllTasks():
    result = [DatabaseEncoder.default(i) for i in Task.query.all()]
    return jsonify(result)

@api_routes.route("/task/<taskID>", methods=['GET','POST','PUT','DELETE'])
def task(taskID):
    if request.method == 'GET':
        result = DatabaseEncoder.default(Task.query.get(taskID))
        print(result)
        if result == None:
            abort(404, "Task Not Found")
        else:
            return result
    if request.method == 'POST':
        if not request.args.get("name") or not request.args.get("description"):
            abort(400)
        if not Task.query.get(taskID):
            name = str(request.args.get("name")).replace('"','')
            description = str(request.args.get("description")).replace('"','')
            db.session.add(Task(taskID = taskID, name=name, description=description))
            db.session.commit()
            return DatabaseEncoder.default(Task.query.get(taskID))
        else:
            abort(409)
    if request.method == 'DELETE':
        if Task.query.get(taskID):
            x = db.session.query(Task).get(taskID)
            db.session.delete(x)
            db.session.commit()
            
            return "OK"
        else:
            abort(400)

@api_routes.route("/team", methods=['GET'])
def AllTeams():
    result = [DatabaseEncoder.default(i) for i in Team.query.all()]
    return jsonify(result)


@api_routes.route("/team/<teamID>", methods=['GET','POST','PUT','DELETE'])
def team(teamID):
    if request.method == 'GET':
        result = DatabaseEncoder.default(Team.query.get(teamID))
        if result == None:
            abort(404, "Team Not Found")
        else:
            return result
    if request.method == 'POST':
        if not request.args.get("name"):
            abort(400)
        if not Team.query.get(teamID):
            db.session.add(Team(teamID = teamID, name=str(request.args.get("name"))))
            db.session.commit()
            return DatabaseEncoder.default(Team.query.get(teamID))
        else:
            abort(409)
    if request.method == 'DELETE':
        if Team.query.get(teamID):
            x = db.session.query(Team).get(teamID)
            db.session.delete(x)
            db.session.commit()
            
            return "OK"
        else:
            abort(400)

@api_routes.route("/assignTask/<taskID>", methods=['PUT'])
def assignTask(taskID):

    pass