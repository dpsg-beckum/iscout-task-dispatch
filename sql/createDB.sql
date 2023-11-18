drop database if exists iScout;
create database IF NOT EXISTS iScout;
use iScout;
create table Status (
	statusID int primary key not null unique,
    name tinytext
);
insert into Status values 
	(1, "Created"),
    (2, "Assigned"),
    (3, "Work in Progress"),
    (4, "Done"),
    (5, "Failed");

create table Team (
	teamID int not null primary key unique,
    name tinytext
);
create table Task (
	taskID int primary key not null unique,
    name tinytext,
    description longtext,
    teamID int,
    foreign key (teamID) references Team(teamID)
);
create table TaskHasStatus (
	taskstatusID int not null primary key auto_increment,
	taskID int not null,
    statusID int not null,
    timestamp datetime,
    foreign key (taskID) references Task(taskID),
    foreign key (statusID) references Status(statusID)
);




#show tables;
#show columns from Task;
show columns from TaskHasStatus;
select * from Task;
select * from TaskHasStatus;