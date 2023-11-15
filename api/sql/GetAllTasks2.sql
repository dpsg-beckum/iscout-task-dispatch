SELECT 
    Task.task_id,
    Task.name,
    Task.description,
    Status.name AS status,
    TaskHasStatus.timestamp,
    Team.team_id,
    Team.name AS team_name
FROM
    Task
        INNER JOIN
    TaskHasStatus ON TaskHasStatus.task_id = Task.task_id
        INNER JOIN
    Status ON TaskHasStatus.status_id = Status.status_id
        LEFT JOIN
    Team ON Task.team_id = Team.team_id
        INNER JOIN
    (SELECT 
        MAX(TaskHasStatus.taskStatus_id) AS taskStatus_id,
            TaskHasStatus.task_id
    FROM
        TaskHasStatus
    GROUP BY TaskHasStatus.task_id) AS latestStatus ON latestStatus.taskStatus_id = TaskHasStatus.taskStatus_id;