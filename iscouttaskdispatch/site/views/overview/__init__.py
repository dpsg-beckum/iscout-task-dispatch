# site/views/overview.py
from flask import render_template, request, redirect, url_for, jsonify, abort
from ....database.handel import *
from ....database.json_encoder import JSONEncoder
from ....tools import formatDatetime, convert_text_to_links
from flask import Blueprint
from pprint import pprint
import time
from datetime import datetime


overview_site = Blueprint("overview_site", __name__, url_prefix="/overview")


@overview_site.route("/")
def index():
    return render_template("overview/index.html")

@overview_site.route("/editor")
def editor():
    return render_template("overview/editor.html")
