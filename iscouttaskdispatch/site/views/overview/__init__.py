# site/views/overview.py
import time
from datetime import datetime
from pprint import pprint

from flask import (Blueprint, abort, jsonify, redirect, render_template,
                   request, url_for)

from ....tools import convert_text_to_links, formatDatetime

overview_site = Blueprint("overview", __name__, url_prefix="/overview")


@overview_site.route("/")
def index():
    return render_template("overview/index.html")


@overview_site.route("/editor")
def editor():
    return render_template("overview/editor.html")
