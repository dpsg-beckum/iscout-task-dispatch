from flask import Blueprint, abort, redirect, render_template, request, url_for

from ....database.db import Task, Team

teams_site = Blueprint("teams_site", __name__,
                       template_folder="../templates/team", url_prefix="/teams")


@teams_site.route("/")
def index():
    teams = getAllTeams()
    return render_template("spielleitung/teams/index.html", teams=teams)


@teams_site.route("/create", methods=["GET", "POST"])
def createTeamSite():
    error_message = None
    form_data = {"teamID": None, "name": "", "desc": ""}

    if request.method == "POST":
        form_data["teamID"] = int(request.form.get("teamID"))
        form_data["name"] = request.form.get("name")
        form_data["desc"] = request.form.get("desc")

        try:
            createTeam(form_data["teamID"],
                       form_data["name"], form_data["desc"])
            return redirect(url_for(".index"))
        except ElementAlreadyExists:
            error_message = "Team with the provided ID already exists."
        except Exception as ex:
            error_message = str(ex)

    return render_template("spielleitung/teams/create.html", error_message=error_message, form_data=form_data)


@teams_site.route("/<int:teamID>/delete", methods=["POST"])
def deleteTeamSite(teamID):
    error_message = None
    if request.method == "POST":
        try:
            deleteTeam(teamID)
            return redirect(url_for(".index"))
        except ElementDoesNotExsist:
            error_message = "Team with the provided ID does not exists."
            # You can handle the error as needed, such as displaying a message to the user.

    return render_template("error.html", error_message=error_message)


@teams_site.route("/<int:teamID>")
def showTeam(teamID):
    return render_template("spielleitung/teams/team.html", team=getTeamViaID(teamID))


@teams_site.route("/<int:teamID>/edit", methods=["GET", "POST"])
def editTeam(teamID):
    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        if name:
            updateTeam(teamID, name, desc)
            return redirect(url_for(".index"))
        else:
            abort(400)

    team = getTeamViaID(teamID)
    if team:
        return render_template("spielleitung/teams/edit.html", team=team)
    else:
        return render_template("error.html", error_message="Task does not exist.")
