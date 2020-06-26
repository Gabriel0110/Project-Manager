# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_project_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial


class Ui_CreateProjectWindow(object):
    def setupUi(self, CreateProjectWindow):
        CreateProjectWindow.setObjectName("CreateProjectWindow")
        CreateProjectWindow.resize(486, 552)
        CreateProjectWindow.setFixedSize(486, 552)
        font = QtGui.QFont()
        font.setPointSize(8)
        CreateProjectWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(CreateProjectWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 40, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.project_name_label = QtWidgets.QLabel(self.centralwidget)
        self.project_name_label.setGeometry(QtCore.QRect(70, 150, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.project_name_label.setFont(font)
        self.project_name_label.setObjectName("project_name_label")
        self.project_desc_label = QtWidgets.QLabel(self.centralwidget)
        self.project_desc_label.setGeometry(QtCore.QRect(30, 290, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.project_desc_label.setFont(font)
        self.project_desc_label.setObjectName("project_desc_label")
        self.desc_plaintext_widget = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.desc_plaintext_widget.setGeometry(QtCore.QRect(190, 260, 221, 78))
        self.desc_plaintext_widget.setObjectName("desc_plaintext_widget")
        self.project_name_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.project_name_edit.setGeometry(QtCore.QRect(190, 150, 221, 22))
        self.project_name_edit.setObjectName("project_name_edit")
        self.create_button = QtWidgets.QPushButton(self.centralwidget)
        self.create_button.setGeometry(QtCore.QRect(190, 400, 93, 28))
        self.create_button.setObjectName("create_button")
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setGeometry(QtCore.QRect(190, 460, 93, 28))
        self.cancel_button.setObjectName("cancel_button")
        CreateProjectWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CreateProjectWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 486, 22))
        self.menubar.setObjectName("menubar")
        CreateProjectWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CreateProjectWindow)
        self.statusbar.setObjectName("statusbar")
        CreateProjectWindow.setStatusBar(self.statusbar)

        self.retranslateUi(CreateProjectWindow)

        self.create_button.clicked.connect(partial(CreateProjectWindow.create, self.project_name_edit, self.desc_plaintext_widget))

        QtCore.QMetaObject.connectSlotsByName(CreateProjectWindow)

    def retranslateUi(self, CreateProjectWindow):
        _translate = QtCore.QCoreApplication.translate
        CreateProjectWindow.setWindowTitle(_translate("CreateProjectWindow", "Create Project"))
        self.label.setText(_translate("CreateProjectWindow", "New Project"))
        self.project_name_label.setText(_translate("CreateProjectWindow", "Project Name: "))
        self.project_desc_label.setText(_translate("CreateProjectWindow", "Project Description: "))
        self.create_button.setText(_translate("CreateProjectWindow", "Create"))
        self.cancel_button.setText(_translate("CreateProjectWindow", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CreateProjectWindow = QtWidgets.QMainWindow()
    ui = Ui_CreateProjectWindow()
    ui.setupUi(CreateProjectWindow)
    CreateProjectWindow.show()
    sys.exit(app.exec_())
