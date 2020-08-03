# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project_window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial


class Ui_ProjectWindow(object):
    def setupUi(self, ProjectWindow):
        ProjectWindow.setObjectName("ProjectWindow")
        ProjectWindow.resize(793, 600)
        ProjectWindow.setFixedSize(793, 600)
        self.centralwidget = QtWidgets.QWidget(ProjectWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.project_name_label = QtWidgets.QLabel(self.centralwidget)
        self.project_name_label.setGeometry(QtCore.QRect(130, 10, 541, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.project_name_label.setFont(font)
        self.project_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.project_name_label.setObjectName("project_name_label")
        self.project_description_label = QtWidgets.QLabel(self.centralwidget)
        self.project_description_label.setGeometry(QtCore.QRect(130, 70, 541, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.project_description_label.setFont(font)
        self.project_description_label.setAlignment(QtCore.Qt.AlignCenter)
        self.project_description_label.setWordWrap(True)
        self.project_description_label.setObjectName("project_description_label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(7, 140, 781, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 180, 311, 211))
        self.groupBox.setObjectName("groupBox")
        self.task_list_widget = QtWidgets.QListWidget(self.groupBox)
        self.task_list_widget.setGeometry(QtCore.QRect(10, 20, 291, 181))
        self.task_list_widget.setObjectName("task_list_widget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(460, 180, 311, 211))
        self.groupBox_2.setObjectName("groupBox_2")
        self.issue_list_widget = QtWidgets.QListWidget(self.groupBox_2)
        self.issue_list_widget.setGeometry(QtCore.QRect(10, 20, 291, 181))
        self.issue_list_widget.setObjectName("issue_list_widget")
        self.create_new_task_button = QtWidgets.QPushButton(self.centralwidget)
        self.create_new_task_button.setGeometry(QtCore.QRect(40, 400, 101, 23))
        self.create_new_task_button.setObjectName("create_new_task_button")
        self.open_selected_task_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_selected_task_button.setGeometry(QtCore.QRect(214, 400, 101, 23))
        self.open_selected_task_button.setObjectName("open_selected_task_button")
        self.open_selected_issue_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_selected_issue_button.setGeometry(QtCore.QRect(644, 400, 111, 23))
        self.open_selected_issue_button.setObjectName("open_selected_issue_button")
        self.create_new_issue_button = QtWidgets.QPushButton(self.centralwidget)
        self.create_new_issue_button.setGeometry(QtCore.QRect(480, 400, 111, 23))
        self.create_new_issue_button.setObjectName("create_new_issue_button")
        self.close_project_button = QtWidgets.QPushButton(self.centralwidget)
        self.close_project_button.setGeometry(QtCore.QRect(710, 10, 75, 23))
        self.close_project_button.setObjectName("close_project_button")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(680, 469, 111, 91))
        self.groupBox_3.setObjectName("groupBox_3")
        self.delete_project_button = QtWidgets.QPushButton(self.groupBox_3)
        self.delete_project_button.setGeometry(QtCore.QRect(20, 60, 75, 23))
        self.delete_project_button.setObjectName("delete_project_button")
        self.delete_checkbox_one = QtWidgets.QCheckBox(self.groupBox_3)
        self.delete_checkbox_one.setGeometry(QtCore.QRect(20, 20, 71, 18))
        self.delete_checkbox_one.setObjectName("delete_checkbox_one")
        self.delete_checkbox_two = QtWidgets.QCheckBox(self.groupBox_3)
        self.delete_checkbox_two.setGeometry(QtCore.QRect(20, 40, 81, 18))
        self.delete_checkbox_two.setObjectName("delete_checkbox_two")
        self.email_button = QtWidgets.QPushButton(self.centralwidget)
        self.email_button.setGeometry(QtCore.QRect(10, 10, 81, 23))
        self.email_button.setObjectName("email_button")
        self.complete_project_button = QtWidgets.QPushButton(self.centralwidget)
        self.complete_project_button.setGeometry(QtCore.QRect(310, 500, 181, 28))
        self.complete_project_button.setObjectName("complete_project_button")
        ProjectWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ProjectWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 793, 25))
        self.menubar.setObjectName("menubar")
        ProjectWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ProjectWindow)
        self.statusbar.setObjectName("statusbar")
        ProjectWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ProjectWindow)

        self.close_project_button.clicked.connect(ProjectWindow.closeProject)
        self.create_new_task_button.clicked.connect(ProjectWindow.createTask)
        #self.create_new_issue_button.clicked.connect(ProjectWindow.createIssue)
        self.delete_project_button.clicked.connect(partial(ProjectWindow.deleteProject, self.delete_checkbox_one, self.delete_checkbox_two))
        #self.email_button.clicked.connect(ProjectWindow.sendEmail)

        QtCore.QMetaObject.connectSlotsByName(ProjectWindow)

    def retranslateUi(self, ProjectWindow):
        _translate = QtCore.QCoreApplication.translate
        ProjectWindow.setWindowTitle(_translate("ProjectWindow", "MainWindow"))
        self.project_name_label.setText(_translate("ProjectWindow", "[Project Name]"))
        self.project_description_label.setText(_translate("ProjectWindow", "[Project Description]"))
        self.groupBox.setTitle(_translate("ProjectWindow", "Tasks"))
        self.groupBox_2.setTitle(_translate("ProjectWindow", "Issues"))
        self.create_new_task_button.setText(_translate("ProjectWindow", "Create New Task"))
        self.open_selected_task_button.setText(_translate("ProjectWindow", "Open Selected Task"))
        self.open_selected_issue_button.setText(_translate("ProjectWindow", "Open Selected Issue"))
        self.create_new_issue_button.setText(_translate("ProjectWindow", "Create New Issue"))
        self.close_project_button.setText(_translate("ProjectWindow", "Close Project"))
        self.groupBox_3.setTitle(_translate("ProjectWindow", "DeleteProject"))
        self.delete_project_button.setText(_translate("ProjectWindow", "Delete Me"))
        self.delete_checkbox_one.setText(_translate("ProjectWindow", "Delete"))
        self.delete_checkbox_two.setText(_translate("ProjectWindow", "Yes, Delete"))
        self.email_button.setText(_translate("ProjectWindow", "Email Reminder"))
        self.complete_project_button.setText(_translate("ProjectWindow", "Complete Project"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ProjectWindow = QtWidgets.QMainWindow()
    ui = Ui_ProjectWindow()
    ui.setupUi(ProjectWindow)
    ProjectWindow.show()
    sys.exit(app.exec_())
