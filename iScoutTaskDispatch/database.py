import mysql.connector
import logging
from datetime import datetime, timedelta
from pprint import pprint
from exeptions import *
import os

class dbInterface():
  def __init__(self) -> None:
    self.__mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root",
      database="iScout"
    )

    self.__folder_path = "./api/sql"
    sql_files = [f for f in os.listdir(self.__folder_path) if f.endswith('.sql')]
    
    self.__sql_dict = {}
    
    for sql_file in sql_files:
        file_path = os.path.join(self.__folder_path, sql_file)
        with open(file_path, 'r') as file:
            content = file.read()
            file_name = os.path.splitext(sql_file)[0]
            self.__sql_dict[file_name] = content
    pass

  def __dbCommit(self, sql:str):
    mycursor = self.__mydb.cursor()
    mycursor.execute(sql)
    self.__mydb.commit()
    return mycursor


  def setTaskName(self, taskID: int, name: str):
    try:
      self.__dbCommit(f'UPDATE Task SET name = "{name}" WHERE taskID = {taskID}')
      #print(mycursor.rowcount, "record inserted.")
    except mysql.connector.errors.IntegrityError:
      raise DBerror("Proably no key")


  def setTaskDescription(self, taskID: int, description: str):
    try:
      self.__dbCommit(f'UPDATE Task SET description = "{description}" WHERE taskID = {taskID}')
      #print(mycursor.rowcount, "record inserted.")
    except mysql.connector.errors.IntegrityError:
      raise DBerror("Proably no key")


  def setTaskStatus(self, taskID: int, statusID: int):
    try:
      self.__dbCommit(f'INSERT INTO TaskHasStatus (taskID, statusID, timestamp) VALUES ({taskID}, {statusID}, "{datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")}")')
      # print(mycursor.rowcount, "record inserted.")
    except mysql.connector.errors.IntegrityError:
      raise DuplicateEntry("Key already Exists")
    

  def createTask(self, taskID: int, name = "", description = ""):
    """
    Creats Task if not exists
    """
    
    try:
      self.__dbCommit(f'INSERT INTO Task (taskID) VALUES ({taskID})')
    except mysql.connector.errors.IntegrityError as ex:
      # logging.error("already Exists")
      raise DuplicateEntry("Task already Exists")
    
    self.setTaskStatus(taskID,1)
    self.setTaskName(taskID, name)
    self.setTaskDescription(taskID, description)


  def getAllTasks(self):
    mycursor = self.__mydb.cursor()

    mycursor.execute(self.__sql_dict["GetAllTasks2"])

    myresult = mycursor.fetchall()

    columns = [col[0] for col in mycursor.description]  # Fetch column names
    result_list = [dict(zip(columns, row)) for row in myresult]

    return result_list


  def createTeam(self, teamID:int, name:str):
    try:
      self.__dbCommit(f'INSERT INTO Team (teamID, name) VALUES ({teamID}, "{name}")')
    except mysql.connector.errors.IntegrityError:
      raise DuplicateEntry("Key already Exists")


  def asignTask(self, taskID: int, teamID: int):
    try:
      self.__dbCommit(f'UPDATE Task SET teamID = {teamID} WHERE taskID = {taskID}')
    except mysql.connector.errors.IntegrityError:
      raise DBerror("Probobly no Team")
    self.setTaskStatus(taskID, 2)


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)

  db = dbInterface()
  try:
    db.createTask(1, "Group photo", 
             """TEXT""")
  
    db.createTask(2, "The Umbrella Trick", """TEXT""")
    db.createTask(3, "Four legs", """TEXT""")
  except DuplicateEntry:
    print("task already inserted")
  
  try:
    db.createTeam(1, "team1")
    db.createTeam(2, "team2")
    db.createTeam(3, "team3")
  except DuplicateEntry:
    print("Teams already exist")
  
  db.asignTask(1,1)
  db.asignTask(2,2)
  db.asignTask(3,2)
  db.asignTask(1,2)


  pprint(db.getAllTasks())

  # try:
  #   createTask(2)
  # except Exception as ex:
  #   logging.error(str(ex))
