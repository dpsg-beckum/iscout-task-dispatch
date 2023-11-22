from datetime import datetime as dt
from datetime import date
from flask import request, Response, jsonify, Blueprint, redirect,flash,render_template,abort
from flask.helpers import url_for
from flask.templating import render_template
from sqlalchemy import desc
from pprint import pprint
from .database.handel import *
from .site.views.tools import formatDatetime 
from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import create_engine, MetaData

site = Blueprint("site", __name__, template_folder="templates")

@site.route("/")
def index():
    return render_template("index.html")


@site.route("/db/ta")
def dbTa():
    return getAllTasks()

@site.route("/db/tast")
def dbTast():
    return getAllTaskHasStatus()