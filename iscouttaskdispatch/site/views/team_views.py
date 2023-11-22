# site/views/team_views.py
from flask import render_template, request, redirect, url_for, abort
from ...database.handel import *
from flask import Blueprint

teams_site = Blueprint("teams_site", __name__, template_folder="../templates/team")

# ... (your existing team-related routes go here)

@teams_site.route("/teams")
def showAllTeams():
    teams = getAllTeams()
    return render_template("team/index.html", teams=teams)

@teams_site.route("/teams/create", methods=["GET", "POST"])
def createTeamSite():
    error_message = None
    form_data = {"teamID": None, "name": ""}

    if request.method == "POST":
        form_data["teamID"] = int(request.form.get("teamID"))
        form_data["name"] = request.form.get("name")

        try:
            createTeam(form_data["teamID"], form_data["name"])
            return redirect(url_for("site.teams_site.showAllTeams"))
        except ElementAlreadyExists:
            error_message = "Team with the provided ID already exists."

    return render_template("team/create.html", error_message=error_message, form_data=form_data)

@teams_site.route("/teams/delete", methods=["GET", "POST"])
def deleteTeamSite():
    error_message = None
    if request.method == "POST":
        teamID = int(request.form.get("teamID"))

        try:
            deleteTeam(teamID)
            return redirect(url_for("site.teams_site.showAllTeams"))
        except ElementDoesNotExsist:
            error_message = "Team with the provided ID does not exists."
            # You can handle the error as needed, such as displaying a message to the user.

    return render_template("team/delete.html", error_message=error_message)


@teams_site.route("/teams/<int:teamID>")
def showTeam(teamID):
    return render_template("team/team.html", team=getTeamViaID(teamID))


@teams_site.route("/teams/<int:teamID>/edit")
def editTeam(teamID):
    team = getTaskViaID(teamID)
    return render_template("team/edit.html", team=team)

@teams_site.route("/teams/<int:teamID>/update", methods=["POST"])
def updateTeam(teamID):
    name = request.form.get("name")
    if name:
        setTeamName(teamID, name)
    else:
        abort(400)

    return redirect(url_for("site.teams_site.showAllTeams"))