from .socket_setup import socketio

def updateOverviewData():
    from ..database.handel import getAllTeams, getAllTasks, getStatusOfTask, getAllStatuses
    from ..site.views.tools import formatDatetime
    teams = {i['teamID']:i['name'] for i in getAllTeams()}
    tasks = getAllTasks()

    allStatuses = getAllStatuses()
    values = [0 for i in range(len(allStatuses.keys()))]
    statuses = [v for k,v in allStatuses.items()]

    for task in tasks:
        task['description'] = task['description'].replace("\r", "").replace("\n","<br>")
        task['teamName'] = teams[task['teamID']] if task['teamID'] != None else "Kein Team Ausgewählt"
        status = getStatusOfTask(task['taskID'])
        task['status'] = status['name']
        task['statusText'] = status['text']
        task['statustimestamp'] = formatDatetime(status['timestamp'])

        key = getStatusOfTask(task['taskID'])['statusID'] -1
        if key != -1:
            values[key] += 1
    
    piechart = {'values': values, 'labels': statuses,
        'type': 'pie',
        'textinfo': "label+value",
        'textposition': "inside",
        'insidetextorientation': "radial",
        'automargin': True}
    
    out = {"piechart": piechart,
           "tasks": tasks,
           "statuses": getAllStatuses()}
    socketio.emit("overview_data", out)