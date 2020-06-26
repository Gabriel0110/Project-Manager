import sys
import time
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial

import Database
from login_ui import Ui_Login
from main_ui import Ui_MainWindow
from create_account_ui import Ui_CreateAccount
from create_project_ui import Ui_CreateProjectWindow
from project_window_ui import Ui_ProjectWindow
import driver

# Who is logged in
CURRENT_USERNAME = ""

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.selected_project = ""

        self.projects = db.getProjects()
        self.populateProjectList(self.projects)

    def populateProjectList(self, projects):
        ''' Load listwidget with project names '''
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
        self.hide()
        self.project_window = ProjectWindow(project)
        self.project_window.show()

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
        username = user.text()
        password = pw.text()

        process = driver.processLogin(username, password)

        if process:
            self.hide()
            self.main_window = MainWindow()
            self.main_window.show()

class ProjectWindow(QtWidgets.QMainWindow):
    def __init__(self, project):
        super().__init__()
        self.ui = Ui_ProjectWindow()
        self.ui.setupUi(self)
        self.current_project = project
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

if __name__ == '__main__':
    # Initialize database at startup
    db = Database.Database()

    app = QtWidgets.QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec_())