import sys
import time
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial

import Database
from login_ui import Ui_Login
from main_ui import Ui_MainWindow
from create_account_ui import Ui_CreateAccount
import driver

# Who is logged in
CURRENT_USERNAME = ""

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        projects = db.getProjects()
        self.populateProjectList(projects)

    def populateProjectList(self, projects):
        ''' Load listwidget with project names '''
        for project_id, project_info in projects.items():
            item = QtWidgets.QListWidgetItem(f"{project_info['project_name']}")
            Ui_MainWindow.listWidget.addItem(item)

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

if __name__ == '__main__':
    # Initialize database at startup
    db = Database.Database()

    app = QtWidgets.QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec_())