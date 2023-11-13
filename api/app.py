from flask import Flask, request, jsonify, abort, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
import json
import redis
from pprint import pprint
import time

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    protocol=3,
    charset="utf-8",
    decode_responses=True,
)

app = Flask(__name__)
CORS(app)
api = Api(app)


def createTask(task_id: int):
    """
    Creats Task if not exists
    """
    key = f"task:{task_id}"

    if r.exists(key):
        return False

    results = []
    results.append(r.hset(key, mapping={"description": "NO TEXT"}))
    results.append(r.hset(key, mapping={"status": "created"}))
    results.append(r.hset(key, mapping={"team": int(0)}))
    # results.append(r.hset(key, mapping={"nr":}))
    results.append(r.hset(key, mapping={"lastupdated": int(time.time())}))

    for result in results:
        if not result:
            return False
    return True


def updateTask(task_id: int, args: dict):
    """
    Updates a Task, Creats one if not Exists
    """
    key = f"task:{task_id}"
    if not r.exists(key):
        # if not createTask(task_id):
        #     return False
        return False

    results = []

    updateHashValue(key,args,"description")
    updateHashValue(key,args,"status")
    updateHashValue(key,args,"team", int)

    # if "description" in args.keys():
    #     results.append(r.hset(key, mapping={"description": str(args["description"])}))
    # if "status" in args.keys():
    #     results.append(r.hset(key, mapping={"status": str(args["status"])}))
    # if "team" in args.keys():
    #     results.append(r.hset(key, mapping={"team": int(args["team"])}))
    # if 'nr' in args.keys():
    #     results.append(r.hset(key, mapping={"nr":int(args['nr'])}))

    r.hset(key, mapping={"lastupdated": int(time.time())})

    return True


def getTask(task_id):
    return r.hgetall(f"task:{task_id}")


def updateHashValue(key: str, datadict: dict, arg: str, datatype = str):
    if arg in datadict.keys():
        if not r.exists(key):
            return False
        data = datadict[arg]
        val = datatype(data)
        r.hset(key, mapping={arg: val})
        return True
    else:
        return None


class Task(Resource):
    def get(self, task_id=None):
        if task_id is None:
            key = "task:*"
            result = [str(i).replace("task:", "") for i in r.keys(key)]
            print(result)
            response = {"task_id": result}
            if response:
                return response
            else:
                return abort(500)
        else:
            result = getTask(task_id)
            print(result)
            if result.keys():
                return jsonify(result)
            else:
                return abort(404)

    def patch(self, task_id=None):
        if task_id:
            if updateTask(task_id, request.form):
                return "OK", 200
            else:
                return abort(500)
        else:
            return abort(405)

    def put(self, task_id=None):
        if task_id:
            if createTask(task_id):
                updateTask(task_id, request.form)
                return "OK", 200
            else:
                return abort(400)
        else:
            return abort(405)

    def delete(self, task_id=None):
        print(task_id)
        if not task_id == None:
            numkeys = r.delete(f"task:{task_id}")
            respond = r'{"keysDeleted":' + str(numkeys) + "}"
            return jsonify(respond)
        else:
            return abort(405)


class Team(Resource):
    def get(self, team_id=None):
        if team_id == None:
            key = "team:*"
            result = r.keys(key)
            return jsonify({"team": result})
        else:
            key = f"team:{team_id}"
            return r.hgetall(key)

    def patch(self, team_id):
        key = f"team:{team_id}"

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

    def put(self, team_id):
        if (not team_id) or (not "name" in request.form.keys()):
            return abort(405)

        key = f"team:{team_id}"

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

    def delete(self, team_id=None):
        print(team_id)
        if not team_id == None:
            numkeys = r.delete(f"team:{team_id}")
            respond = r'{"keysDeleted":' + str(numkeys) + "}"
            return respond, 200
        else:
            return abort(405)

@app.route('/tasksDashboard')
def serve_html():
    return render_template('tasksDashboard.html')


api.add_resource(Task, *["/api/task", "/api/task/<task_id>"])
api.add_resource(Team, *["/api/team", "/api/team/<team_id>"])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
