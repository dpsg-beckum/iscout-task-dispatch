from flask import Blueprint


api_routes = Blueprint("api", __name__, template_folder="templates",
                       url_prefix="")



@api_routes.route("/task", methods=['GET'])
def getAllTasks():
    return "Task"

@api_routes.route("/task/<taskID>", methods=['GET','POST','PUT','DELETE'])
def getTask(taskID):
    return "Task via ID"

@api_routes.route("/team", methods=['GET'])
def getAllTeams():
    return "Team"

@api_routes.route("/team/<teamID>", methods=['GET','POST','PUT','DELETE'])
def getTeam(teamID):
    return "Team via ID"