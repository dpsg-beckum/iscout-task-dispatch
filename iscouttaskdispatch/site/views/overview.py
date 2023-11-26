# site/views/overview.py
from flask import render_template, request, redirect, url_for
from flask_socketio import emit
from ...database.handel import *
from .tools import formatDatetime
from flask import Blueprint
from pprint import pprint
import time
from datetime import datetime

from ...sockets.socket_setup import socketio
from ...sockets.sockethelper import updateOverviewData

overview_site = Blueprint("overview_site", __name__, template_folder="../templates/overview", url_prefix="/overview")

@overview_site.route("/")
def showOverview():
    

    return render_template("overview/index.html")


@socketio.on('get_overview_data')
def get_time():
    updateOverviewData()
    pass
    # while True:
    #     current_time = datetime.now().strftime('%H:%M:%S')
    #     socketio.emit('update_time', {'time': current_time})
    #     time.sleep(5)