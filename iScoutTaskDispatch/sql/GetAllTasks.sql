SELECT
    taskID,
    name,
    description,
    teamID,
    team_name,
    status,
    timestamp
FROM (
    SELECT
        Task.taskID,
        Task.name,
        Task.description,
        Status.name AS status,
        TaskHasStatus.timestamp,
        Team.teamID,
        Team.name AS team_name,
        ROW_NUMBER() OVER (PARTITION BY Task.taskID ORDER BY TaskHasStatus.timestamp DESC) AS rn
    FROM
        Task
        INNER JOIN TaskHasStatus ON TaskHasStatus.taskID = Task.taskID
        INNER JOIN Status ON TaskHasStatus.statusID = Status.statusID
        LEFT JOIN Team ON Task.teamID = Team.teamID
) AS RankedTaskStatus
WHERE
    rn = 1;