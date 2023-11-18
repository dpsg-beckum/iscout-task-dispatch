from flask import Flask, request, jsonify, abort, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
import json
from pprint import pprint
import time
from database import dbInterface

db = dbInterface()

app = Flask(__name__)
CORS(app)
api = Api(app)



@app.route("/task", methodes=['GET'])
def getTasks(self, taskID=None):
    if taskID is None:
        
        try:
            results = db.getAllTasks()
            return jsonify(results)
        except:
            return abort(500)
    else:
        try:
            results = db.getAllTasks()
            for result in results:
                if result['taskID'] == taskID:
                    return jsonify(result)
            return abort(404)
        except Exception as ex:
            return str(ex), 500

@app.routs("/task/<taskID>", methodes=['PATCH'])
def updateTask(self, taskID=None):
    if taskID:
        if updateTask(taskID, request.form):
            return "OK", 200
        else:
            return abort(500)
    else:
        return abort(405)

@app.route("/task/<taskID>", methodes=['PUT'])
def createTask(self, taskID=None):
    if taskID:
        if db.createTask(taskID):
            updateTask(taskID, request.form)
            request
            return "OK", 200
        else:
            return abort(400)
    else:
        return abort(405)

@app.route("/task/<taskID>", methodes=['DELETE'])
def delete(self, taskID=None):
    print(taskID)
    if not taskID == None:
        numkeys = r.delete(f"task:{taskID}")
        respond = '{"keysDeleted":' + str(numkeys) + "}"
        return jsonify(respond)
    else:
        return abort(405)


@app.route("/team", methodes=['GET'])
def getAllTeams(self, teamID=None):
    if teamID == None:
        key = "team:*"
        result = r.keys(key)
        return jsonify({"team": result})
    else:
        key = f"team:{teamID}"
        return r.hgetall(key)

@app.route("/team/<teamID>", methodes=['GET'])
def getTeamInfo(self, teamID):
    key = f"team:{teamID}"

    if not r.exists(key):
        return abort(404)

    args = dict(request.form)

    updateHashValue(key, args, "currenttask", int)
    updateHashValue(key, args, "nexttask", int)

    # if "currenttask" in args.keys():
    #     r.hset(key, mapping={"currenttask": int(args["description"])})
    # if "nexttask" in args.keys():
    #     r.hset(key, mapping={"nexttask": int(args["nexttask"])})

    return "OK", 200

@app.route("/team/<teamID>", methodes=['PUT'])
def createTeam(self, teamID):
    if (not teamID) or (not "name" in request.form.keys()):
        return abort(405)

    key = f"team:{teamID}"

    if r.exists(key):
        return abort(409)

    args = dict(request.form)

    # r.hset(key, mapping={"name":str(args['name'])})
    # r.hset(key, mapping={"currenttask":int(-1)})
    # r.hset(key, mapping={"nexttask":int(-1)})
    updateHashValue(key, args, "name", str)
    updateHashValue(key, args, "currenttask", int)
    updateHashValue(key, args, "nexttask", int)

    return "OK", 200

@app.route("/team/<teamID>", methodes=['DELETE'])
def deleteTeam(self, teamID=None):
    print(teamID)
    if not teamID == None:
        numkeys = r.delete(f"team:{teamID}")
        respond = r'{"keysDeleted":' + str(numkeys) + "}"
        return respond, 200
    else:
        return abort(405)

@app.route('/tasksDashboard')
def serve_html():
    return render_template('tasksDashboard.html')


# api.add_resource(Task, *["/api/task", "/api/task/<taskID>"])
# api.add_resource(Team, *["/api/team", "/api/team/<teamID>"])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
