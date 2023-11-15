SELECT
    task_id,
    name,
    description,
    team_id,
    team_name,
    status,
    timestamp
FROM (
    SELECT
        Task.task_id,
        Task.name,
        Task.description,
        Status.name AS status,
        TaskHasStatus.timestamp,
        Team.team_id,
        Team.name AS team_name,
        ROW_NUMBER() OVER (PARTITION BY Task.task_id ORDER BY TaskHasStatus.timestamp DESC) AS rn
    FROM
        Task
        INNER JOIN TaskHasStatus ON TaskHasStatus.task_id = Task.task_id
        INNER JOIN Status ON TaskHasStatus.status_id = Status.status_id
        LEFT JOIN Team ON Task.team_id = Team.team_id
) AS RankedTaskStatus
WHERE
    rn = 1;