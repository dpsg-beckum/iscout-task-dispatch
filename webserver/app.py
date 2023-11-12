from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
import json
import redis
from pprint import pprint
import time

r = redis.Redis(host='localhost', port=6379, db=0, protocol=3, charset="utf-8", decode_responses=True)

app = Flask(__name__)
api = Api(app)

def updateTask(task_id, args:dict):
    key = f"task:{task_id}".encode("utf-8").decode("utf-8")
    print(key)
    results = []
    
    if 'description' in args.keys():
        results.append(r.hset(key, mapping={"description":str(args['description'])}))
    if 'status' in args.keys():
        results.append(r.hset(key, mapping={"status":str(args['status'])}))
    if 'team' in args.keys():
        results.append(r.hset(key, mapping={"team":int(args['team'])}))
    if 'nr' in args.keys():
        results.append(r.hset(key, mapping={"nr":int(args['nr'])}))

    results.append(r.hset(key, mapping={"lastupdated":int(time.time())}))

    for result in results:
        if not result:
            return False
    return True

def getTask(task_id):    
    return r.hgetall(f"task:{task_id}")



class Task(Resource):
    def get(self, task_id = None):
        if task_id is None:
            key = "task:*"
            result = r.keys(key)
            response = {"task_id":result}
            if response:
                return response
            else:
                return abort(500)
        else:    
            result = str(getTask(task_id))
            print(result)
            if result:
                return result
            else:
                return abort(418)

    def post(self, task_id = None):
        if task_id:
            if updateTask(task_id, request.form):
                return "OK", 200
            else:
                return abort(500)
        else:
            return abort(405)

class Team(Resource):
    def get(self, team_id = None):
        pass

    def put(self, team_id):
        if not team_id:
            return abort(405)
        

api.add_resource(Task, *['/task', '/task/<task_id>'])
api.add_resource(Team, *['/team', '/team/<team_id>'])


if __name__ == '__main__':
    app.run(debug=True)