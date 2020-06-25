import project_manager
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

        if self.conn is not None:
            self.create_tables(self.conn, [self.create_accounts_table])
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

    def getCurrentMonth(self):
        current_month = datetime.now().month
        if current_month in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            current_month = "0{}".format(current_month)
        else:
            current_month = str(current_month)
        return current_month