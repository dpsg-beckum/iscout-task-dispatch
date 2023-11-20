from flask import Blueprint, request, Response, abort, jsonify
from ..database import handel as database
api_routes = Blueprint("api", __name__, template_folder="templates",
                       url_prefix="")



@api_routes.route("/task", methods=['GET'])
def AllTasks():
    return jsonify(database.getAllTasks())

@api_routes.route("/task/<taskID>", methods=['GET','POST','PUT','DELETE'])
def task(taskID):
    if request.method == 'GET':
        result = database.getTaskViaID(taskID)
        if result == None:
            abort(404, "Task Not Found")
        else:
            return result

    if request.method == 'POST':
        if not request.args.get("name") or not request.args.get("description"):
            abort(400)
        return database.createTask(taskID,
                                   str(request.args.get("name")),
                                   str(request.args.get("description")))
    
    if request.method == 'DELETE':
        return database.deleteTask(taskID)

@api_routes.route("/team", methods=['GET'])
def AllTeams():
    return jsonify(database.getAllTeams())


@api_routes.route("/team/<teamID>", methods=['GET','POST','PUT','DELETE'])
def team(teamID):
    if request.method == 'GET':
        result = database.getTeamViaID(teamID)
        if result == None:
            abort(404, "Team Not Found")
        else:
            return result

    if request.method == 'POST':
        if not request.args.get("name"):
            abort(400)
        return database.createTeam(teamID, name=str(request.args.get("name")))
        
    if request.method == 'DELETE':
        return database.deleteTeam(teamID)

@api_routes.route("/assignTask/<taskID>/<teamID>", methods=['PUT'])
def assignTask(taskID,teamID):
    return database.assignTask(taskID,teamID)