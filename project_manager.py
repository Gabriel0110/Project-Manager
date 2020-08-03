import sys
import time
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import pyautogui as pag
import tkinter as tk
from tkinter import *
from tkinter import filedialog

import Database
import driver
from client import Client

from login_ui import Ui_Login
from main_ui import Ui_MainWindow
from create_account_ui import Ui_CreateAccount
from create_project_ui import Ui_CreateProjectWindow
from project_window_ui import Ui_ProjectWindow
#from create_task_ui import Ui_CreateTaskWindow
#from create_issue_ui import Ui_CreateIssueWindow
from code_editor_ui import Ui_CodeEditorWindow

# Who is logged in
CURRENT_USERNAME = ""

# Active project/file
CURRENT_PROJECT = None
CURRENT_LOADED_FILE = None

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.selected_project = ""

        self.projects = db.getProjects()
        if self.projects:
            self.populateProjectList(self.projects)
        else:
            pass

    def populateProjectList(self, projects):
        for project_id, project_info in projects.items():
            item = QtWidgets.QListWidgetItem(project_info['project_name'])
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.ui.project_list_widget.addItem(item)
                    
    def createProject(self):
        self.hide()
        self.create_project_window = CreateProjectWindow()
        self.create_project_window.show()

    def itemSelected(self, item):
        print(item.text())
        self.selected_project = item.text()

    def openSelectedProject(self):
        project = {proj_id:proj_info for proj_id, proj_info in self.projects.items() if self.selected_project in proj_info.values()}
        #print(project)
        if project:
            self.hide()
            self.project_window = ProjectWindow(project)
            self.project_window.show()

    def openCodeEditor(self):
        self.code_editor_window = CodeEditorWindow()
        self.code_editor_window.show()

    def logout(self):
        global CURRENT_USERNAME
        self.hide()
        self.login_window = LoginWindow()
        CURRENT_USERNAME = ""
        self.login_window.show()

class CreateAccountWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CreateAccount()
        self.ui.setupUi(self)
        self.login_window = LoginWindow()
        self.user_le = self.ui.lineEdit
        self.pass_le = self.ui.lineEdit_2
        self.email_le = self.ui.lineEdit_3

    def loginWindow(self):
        self.hide()
        self.login_window.show()

    def processCreation(self, user, pw, email):
        user = user.text()
        pw = pw.text()
        email = email.text()

        process = driver.processCreation(user, pw, email)

        if process:
            self.hide()
            self.login_window.show()

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.login_info = db.getLoginInfo()

    def createAccountWindow(self):
        self.hide()
        self.create_account_window = CreateAccountWindow()
        self.create_account_window.show()

    def processLogin(self, user, pw):
        global CURRENT_USERNAME
        username = user.text()
        password = pw.text()

        process = driver.processLogin(username, password)

        if process:
            # conn_attempt = CLIENT.connect()
            # if conn_attempt:
            #     self.hide()
            #     self.main_window = MainWindow()
            #     self.main_window.show()
            CURRENT_USERNAME = username
            self.hide()
            self.main_window = MainWindow()
            self.main_window.show()

class ProjectWindow(QtWidgets.QMainWindow):
    def __init__(self, project):
        global CURRENT_PROJECT
        super().__init__()
        self.ui = Ui_ProjectWindow()
        self.ui.setupUi(self)
        self.current_project = project
        CURRENT_PROJECT = self.current_project
        self.loadProject()

    def loadProject(self):
        proj_id = list(self.current_project.keys())[0]
        proj_info = self.current_project[proj_id]
        self.ui.project_name_label.setText(proj_info["project_name"])
        self.ui.project_description_label.setText(proj_info["project_description"])

    def closeProject(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.selected_project = ""
        self.main_window.show()

    def createTask(self):
        self.hide()
        self.create_task_window = CreateTaskWindow()
        self.create_task_window.show()

    def openTask(self):
        pass

    def createIssue(self):
        pass

    def openIssue(self):
        pass

    def deleteProject(self, checkBoxOne, checkBoxTwo):
        global CURRENT_PROJECT
        if checkBoxOne.isChecked() and checkBoxTwo.isChecked():
            self.hide()
            self.main_window = MainWindow()
            proj_id = list(self.current_project.keys())[0]
            proj_info = self.current_project[proj_id]
            proj_name = proj_info['project_name']
            for i in range(self.main_window.ui.project_list_widget.count()):
                if self.main_window.ui.project_list_widget.item(i).text() == proj_name:
                    self.main_window.ui.project_list_widget.takeItem(i)

            self.current_project = None
            CURRENT_PROJECT = None
            self.main_window.projects = db.getProjects()
            self.main_window.show()
            result = driver.deleteProject(proj_name)
        else:
            driver.showDialog("If you really want to throw a project into oblivion, both checkboxes must be checked.", "Whoa whoa")
            return

    def sendEmail(self):
        import smtplib
        global CURRENT_USERNAME
        login_info = db.getLoginInfo()
        email = login_info[CURRENT_USERNAME][1]
        
        sender, receiver = email, email
        message = f"""From: {CURRENT_USERNAME} <{email}>
        To: {CURRENT_USERNAME} <{email}>
        Subject: PROJECT REMINDER: {self.current_project}

        This is a project reminder sent from the Project Manager tool.
        """

        try:
            at = email.find('@')
            dot = email.find('.com')
            smtplib.SMTP(f'mail.{email[at+1:dot]}.com', 25)
            smtpObj = smtplib.SMTP('localhost')
            smptObj.sendmail(sender, receiver, message)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Unable to send email: {e}")

class TaskWindow(QtWidgets.QMainWindow):
    def __init__(self, project, task):
        super().__init__()
        self.ui = Ui_ProjectWindow()
        self.ui.setupUi(self)
        self.current_project = project
        self.current_task = task
        self.loadTask()

    def loadTask(self):
        proj_id = list(self.current_project.keys())[0]
        proj_info = self.current_project[proj_id]
        self.ui.project_name_label.setText(proj_info["project_name"])
        self.ui.project_description_label.setText(proj_info["project_description"])

    def closeTask(self):
        global CURRENT_PROJECT
        self.hide()
        self.project_window = ProjectWindow(CURRENT_PROJECT)
        self.project_window.show()

class CreateProjectWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CreateProjectWindow()
        self.ui.setupUi(self)

    def create(self, proj_name_widget, proj_desc_widget):
        proj_name = proj_name_widget.text()
        proj_desc = proj_desc_widget.toPlainText()

        result = driver.createProject(proj_name, proj_desc)

        if result:
            self.hide()
            self.main_window = MainWindow()
            self.main_window.show()

    def close(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()

class CreateTaskWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CreateTaskWindow()
        self.ui.setupUi(self)

    def create(self, task_name_widget, task_desc_widget):
        global CURRENT_PROJECT
        task_name = task_name_widget.text()
        task_desc = task_desc_widget.toPlainText()

        result = driver.createTask(task_name, task_desc)

        if result:
            self.hide()
            self.project_window = ProjectWindow(CURRENT_PROJECT)
            self.project_window.show()

class CodeEditorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CodeEditorWindow()
        self.ui.setupUi(self)
        #self.current_loaded_file = ""
        self.selected_item = ""

        self.files = db.getFiles()
        if self.files:
            self.populateFileList(self.files)
        else:
            pass

    def populateFileList(self, files):
        ''' Load listwidget with file names '''
        for file_id, file_info in files.items():
            item = QtWidgets.QListWidgetItem(file_info['file_name'])
            self.ui.list_widget.addItem(item)

    def createFile(self):
        global CURRENT_LOADED_FILE
        file_name = pag.prompt(text="Enter a name for the file:\n", title="Enter a name")
        if file_name:
            # add item to database
            try:
                result = driver.insertFile(file_name)
                self.files = db.getFiles()
            except:
                print("FAILED TO INSERT FILE INTO DATABASE")
                return

            if result:
                CURRENT_LOADED_FILE = file_name
                self.selected_item = file_name
                item = QtWidgets.QListWidgetItem(file_name)
                self.ui.list_widget.addItem(item)
                self.ui.list_widget.setCurrentItem(item)
                self.ui.text_edit_widget.setReadOnly(False)
                self.ui.text_edit_widget.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")
                self.ui.text_edit_widget.setPlainText("<Insert Code>")
        else:
            return

    def itemSelected(self, item):
        print(item.text())
        self.selected_item = item.text()

    def loadFile(self):
        global CURRENT_LOADED_FILE
        if not self.selected_item:
            pass
        else:
            contents = self.getFileContents(self.selected_item)
            print(contents)
            self.ui.text_edit_widget.setReadOnly(False)
            self.ui.text_edit_widget.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")
            self.ui.text_edit_widget.setPlainText(contents)
            CURRENT_LOADED_FILE = self.selected_item

    def getFileContents(self, file_name):
        for file_id, file_info in self.files.items():
            if file_info["file_name"] == file_name:
                return self.files[file_id]["file_contents"]

    def getFileInfo(self, file_name):
        for file_id, file_info in self.files.items():
            if file_info["file_name"] == file_name:
                return self.files[file_id]

    def saveUpdate(self):
        global CURRENT_LOADED_FILE
        file_info = self.getFileInfo(CURRENT_LOADED_FILE)
        result = driver.saveFile(CURRENT_LOADED_FILE, self.ui.text_edit_widget.toPlainText(), file_info)
        if result:
            self.files = db.getFiles()
        else:
            pass

    def exportFiles(self):
        import os
        from pathlib import Path

        cwd = os.getcwd()
        if not os.path.exists(cwd + "/exported_code"):
            print("Creating directory folder...")
            Path(f"{cwd}\\exported_code").mkdir(parents=True, exist_ok=True)
            print("Creating files...")
            for file_id, file_info in self.files.items():
                with open(f"{cwd}\\exported_code\\{file_info['file_name']}", "w+") as f:
                    f.write(file_info["file_contents"])
            driver.showDialog("Files were saved in {}".format(cwd + "\\exported_code"), "Files Saved")
        else:
            print("Directory found, creating files...")
            for file_id, file_info in self.files.items():
                with open(f"{cwd}\\exported_code\\{file_info['file_name']}", "w+") as f:
                    f.write(file_info["file_contents"])
            driver.showDialog("Files were saved in {}".format(cwd + "\\exported_code"), "Files Saved")

    def getFileName(self, path):
        import ntpath
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def importFile(self):
        global CURRENT_LOADED_FILE
        filepath = filedialog.askopenfilename(title="Select a Code File", filetypes = (("Python files", "*.py*"), ("Text files", "*.txt*"), ("all files", "*.*")))
        filename = self.getFileName(filepath)
        tk.Tk().destroy()

        for i in range(self.ui.list_widget.count()):
            if self.ui.list_widget.item(i).text() == filepath:
                driver.showDialog("That file is already imported. Delete it first if you want to re-import it, if this is the intended action.", "Already Imported")
                return

        # Read file and get contents
        contents = ""
        with open(filepath, "r") as f:
            for line in f:
                contents += line

        # Create list widget entry for the file
        item = QtWidgets.QListWidgetItem(filename)
        self.ui.list_widget.addItem(item)
        self.ui.list_widget.setCurrentItem(item)

        # Make the selected item the new file in the list
        self.selected_item = filename
        CURRENT_LOADED_FILE = filename

        # Load the contents of the file into the editor with
        self.ui.text_edit_widget.clear()
        self.ui.text_edit_widget.setReadOnly(False)
        self.ui.text_edit_widget.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")
        self.ui.text_edit_widget.setPlainText(contents)

        # Insert into DB
        driver.insertImportedFile(filename, filepath, contents)
        self.files = db.getFiles()

    def deleteFile(self):
        global CURRENT_LOADED_FILE
        if self.selected_item:
            result = driver.deleteFile(self.selected_item)
            if result:
                for i in range(self.ui.list_widget.count()):
                    if self.ui.list_widget.item(i).text() == self.selected_item:
                        item = QtWidgets.QListWidgetItem(self.selected_item)
                        self.ui.list_widget.takeItem(i)
                        if CURRENT_LOADED_FILE == self.selected_item:
                            CURRENT_LOADED_FILE = ""
                            self.ui.text_edit_widget.clear()
                            self.ui.text_edit_widget.setReadOnly(True)
                            self.ui.text_edit_widget.setStyleSheet("background-color: rgb(211, 211, 211);")
                        self.selected_item = ""
                        self.files = db.getFiles()
                        print("Item removed from list")
                        return
            else:
                pass
        else:
            return

if __name__ == '__main__':
    # Initialize database at startup
    db = Database.Database()

    # Active client
    CLIENT = Client()

    app = QtWidgets.QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec_())