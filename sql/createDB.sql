drop database if exists iScout;
create database IF NOT EXISTS iScout;
use iScout;
create table Status (
	status_id int primary key not null unique,
    name tinytext
);
insert into Status values 
	(1, "Created"),
    (2, "Assigned"),
    (3, "Work in Progress"),
    (4, "Done"),
    (5, "Failed");

create table Team (
	team_id int not null primary key unique,
    name tinytext
);
create table Task (
	task_id int primary key not null unique,
    description longtext,
    team_id int,
    foreign key (team_id) references Team(team_id)
);
create table TaskHasStatus (
	task_id int not null,
    status_id int not null,
    timestamp timestamp,
    foreign key (task_id) references Task(task_id),
    foreign key (status_id) references Status(status_id)
);




#show tables;
#show columns from Task;
show columns from TaskHasStatus;