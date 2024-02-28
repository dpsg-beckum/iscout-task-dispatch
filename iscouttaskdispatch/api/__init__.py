from flask import Blueprint, render_template, request, redirect, url_for, abort
from ..database.handel import *

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/")
def index():
    return "OK"


@api.route("/task/create", methods=["POST"])
def createTaskApi():
    try:
        taskID = int(str(request.form.get("taskID")))
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()
        createTask(taskID, name, description, "Created via API")
        return "OK"
    except ValueError:
        return abort(400)
    except ElementAlreadyExists:
        abort(409,"Task with the provided ID already exists.")
    except Exception as ex:
        print(ex)
        abort(500, str(ex))
