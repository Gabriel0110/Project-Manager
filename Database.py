import project_manager as PM
import sqlite3
from sqlite3 import Error
import os
import pyautogui
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.CURRENT_USERNAME = ""

        # Connect to a database, or create + connect at startup
        cwd = os.getcwd()

        self.conn = self.create_connection(cwd + "/project_manager_db.db")

        self.create_accounts_table = """CREATE TABLE IF NOT EXISTS accounts (
                                        username VARCHAR(100) PRIMARY KEY,
                                        password VARCHAR(100) NOT NULL,
                                        email VARCHAR(100) NOT NULL,
                                        creation_date VARCHAR(10) NOT NULL
                                    ); """

        self.create_projects_table = """CREATE TABLE IF NOT EXISTS projects (
                                        project_id INTEGER PRIMARY KEY,
                                        project_owner VARCHAR(100) NOT NULL,
                                        project_name VARCHAR(100) NOT NULL,
                                        project_creation_date VARCHAR(10) NOT NULL,
                                        project_due_date VARCHAR(10),
                                        project_completed_date VARCHAR(10),
                                        project_description VARCHAR(1000),
                                        project_isCompleted INTEGER DEFAULT 0,
                                        project_notes VARCHAR(1000000)
                                    ); """

        self.create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                        task_id INTEGER PRIMARY KEY,
                                        project_id INTEGER NOT NULL,
                                        task_name VARCHAR(100) NOT NULL,
                                        task_creation_date VARCHAR(10) NOT NULL,
                                        task_due_date VARCHAR(10),
                                        task_completed_date VARCHAR(10),
                                        task_description VARCHAR(1000),
                                        task_isCompleted INTEGER DEFAULT 0,
                                        task_notes VARCHAR(1000000)
                                    ); """

        self.create_issues_table = """CREATE TABLE IF NOT EXISTS issues (
                                        issue_id INTEGER PRIMARY KEY,
                                        project_id INTEGER NOT NULL,
                                        issue_name VARCHAR(100) NOT NULL,
                                        issue_creation_date VARCHAR(10) NOT NULL,
                                        issue_completed_date VARCHAR(10),
                                        issue_description VARCHAR(1000),
                                        issue_priority VARCHAR(100),
                                        issue_isCompleted INTEGER DEFAULT 0
                                    ); """

        self.create_code_files_table = """CREATE TABLE IF NOT EXISTS code_files (
                                        file_id INTEGER PRIMARY KEY,
                                        file_owner VARCHAR(100) NOT NULL,
                                        file_name VARCHAR(100) NOT NULL,
                                        file_creation_date VARCHAR(10),
                                        file_last_save_date VARCHAR(10),
                                        file_contents VARCHAR(999999),
                                        file_isImported INTEGER DEFAULT 0,
                                        file_path VARCHAR(1000)
                                    ); """

        if self.conn is not None:
            self.create_tables(self.conn, [self.create_accounts_table, self.create_projects_table, self.create_tasks_table, self.create_issues_table, self.create_code_files_table])
        else:
            print("Error -- no database connection found.")
            exit()

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("Database connection successful!")
            return conn
        except Error as e:
            print(e)
        return conn

    def create_tables(self, conn, tables):
        c = conn.cursor()
        for table in tables:
            try:
                c.execute(table)
            except Error as e:
                print(e)

    def insert(self, insertions):
        c = self.conn.cursor()

        # Loop through all records (entries), inserting each into the database
        for values, query in insertions.items():
            try:
                c.execute(query, values)
                print("Insertion successful!")
            except Error as e:
                print(e)
                return False
        #pyautogui.alert(text = "Insertions successful!", title = "SUCCESS", button = 'OK')
        self.conn.commit()
        return True

    def update(self, query, values):
        c = self.conn.cursor()
        try:
            c.execute(query, values)
            print("Update successful!")
        except Error as e:
            print("Update unsuccessful: {}".format(e))
            return False
        self.conn.commit()
        return True

    def delete(self, query, values):
        c = self.conn.cursor()
        try:
            c.execute(query, values)
            print("Delete successful!")
        except Error as e:
            print("Delete unsuccessful: {}".format(e))
            return False
        self.conn.commit()
        return True

    def insertAccount(self, insertions):
        c = self.conn.cursor()

        # Loop through all records (entries), inserting each into the database
        for values, query in insertions.items():
            try:
                c.execute(query, values)
                print("Insertion successful!")
            except Error as e:
                print(e)
                return False
        #pyautogui.alert(text = "Insertions successful!", title = "SUCCESS", button = 'OK')
        self.conn.commit()
        return True

    def getLoginInfo(self):
        c = self.conn.cursor()
        try:
            info = c.execute("""SELECT username, password, email FROM accounts""").fetchall()

            info_dict = {}
            for (user, pw, email) in info:
                info_dict[user] = [pw, email]
            print("Accounts: {}".format(info_dict))
            return info_dict
        except Error as e:
            print(e)

    def getProjectIds(self):
        c = self.conn.cursor()
        try:
            id_col = c.execute("""SELECT project_id FROM projects""")
            ids = [idx[0] for idx in id_col]
            return ids
        except Error as e:
            print("Could not get projects IDs: {}".format(e))
            return

    def getCurrentMonth(self):
        current_month = datetime.now().month
        if current_month in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            current_month = "0{}".format(current_month)
        else:
            current_month = str(current_month)
        return current_month

    def getProjects(self):
        c = self.conn.cursor()
        try:
            projects = c.execute("""SELECT project_id, project_owner, project_name, project_creation_date, project_due_date, project_completed_date, project_description, 
            project_isCompleted, project_notes FROM projects WHERE project_owner = ?""", (PM.CURRENT_USERNAME,)).fetchall()

            projects_dict = {}
            for (proj_id, proj_owner, proj_name, proj_creation_date, proj_due_date, proj_completed_date, proj_desc, proj_isCompleted, proj_notes) in projects:
                projects_dict[proj_id] = {"project_owner":proj_owner, "project_name":proj_name, "project_creation_date":proj_creation_date, "project_due_date":proj_due_date, "project_completed_date":proj_completed_date, "project_description":proj_desc, "project_isCompleted":proj_isCompleted, "project_notes":proj_notes}
            print("Projects: {}".format(projects_dict))
            return projects_dict
        except Error as e:
            print("Error in getProjects(): {}".format(e))

    def getFiles(self):
        c = self.conn.cursor()
        try:
            files = c.execute("""SELECT file_id, file_owner, file_name, file_creation_date, file_last_save_date, file_contents, file_isImported, file_path FROM code_files WHERE file_owner = ?""", (PM.CURRENT_USERNAME,)).fetchall()

            files_dict = {}
            for (file_id, file_owner, file_name, file_creation_date, file_last_save_date, file_contents, file_isImported, file_path) in files:
                files_dict[file_id] = {"file_owner":file_owner, "file_name":file_name, "file_creation_date":file_creation_date, "file_last_save_date":file_last_save_date, "file_contents":file_contents, "file_isImported":file_isImported, "file_path":file_path}
            print("Files: {}".format(files_dict))
            return files_dict
        except Error as e:
            print("Error in getFiles() in Database.py: {}".format(e))

    def getFileIds(self):
        c = self.conn.cursor()
        try:
            id_col = c.execute("""SELECT file_id FROM code_files""")
            ids = [idx[0] for idx in id_col]
            return ids
        except Error as e:
            print("Could not get file IDs: {}".format(e))
            return

    # def getSelectedProject(self, project):
    #     c = self.conn.cursor()
    #     try:
    #         projects = c.execute("""SELECT project_id, project_name, project_creation_date, project_due_date, project_completed_date, project_description, 
    #         project_isCompleted, project_notes FROM projects""").fetchall()

    #         projects_dict = {}
    #         for (proj_id, proj_name, proj_creation_date, proj_due_date, proj_completed_date, proj_desc, proj_isCompleted, proj_notes) in projects:
    #             projects_dict[proj_id] = {"project_name":proj_name, "project_creation_date":proj_creation_date, "project_due_date":proj_due_date, "project_completed_date":proj_completed_date, "project_description":proj_desc, "project_isCompleted":proj_isCompleted, "project_notes":proj_notes}
    #         print("Projects: {}".format(projects_dict))
    #         return projects_dict
    #     except Error as e:
    #         print(e)