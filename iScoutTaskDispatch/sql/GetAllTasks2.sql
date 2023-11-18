SELECT 
    Task.taskID,
    Task.name,
    Task.description,
    Status.name AS status,
    TaskHasStatus.timestamp,
    Team.teamID,
    Team.name AS team_name
FROM
    Task
        INNER JOIN
    TaskHasStatus ON TaskHasStatus.taskID = Task.taskID
        INNER JOIN
    Status ON TaskHasStatus.statusID = Status.statusID
        LEFT JOIN
    Team ON Task.teamID = Team.teamID
        INNER JOIN
    (SELECT 
        MAX(TaskHasStatus.taskstatusID) AS taskstatusID,
            TaskHasStatus.taskID
    FROM
        TaskHasStatus
    GROUP BY TaskHasStatus.taskID) AS latestStatus ON latestStatus.taskstatusID = TaskHasStatus.taskstatusID;