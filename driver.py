import Database
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog
import pyautogui as pag

import project_manager as PM

# Process account creation
def processCreation(user, pw, email):
    db = Database.Database()

    for item in [user, pw, email]:
        if not item:
            print("Username, password, and email are required!")
            showDialog("Username, password, and email are required!", "Error")
            return
        
    login_info = db.getLoginInfo()
    if user in login_info.keys():
        print("Username already taken.")
        showDialog("That username is already taken!", "Username taken")
        return
    elif any(email in val for val in login_info.values()):
        print("Email already in use.")
        showDialog("That email is already in use!", "Email in use")
        return
    else:
        username = user
        password = pw
        email = email
        date = datetime.now().strftime("%m/%d/%Y")

        values = (username, password, email, date)
        print(values)
        query = """INSERT INTO accounts VALUES (?, ?, ?, ?);"""

        insertions = {values: query}

        insert = db.insertAccount(insertions)
        if insert is True:
            print("Account creation successful!")
            showDialog("Account created!", "Account created")
            return True
        else:
            print("Error with account creation.")
            showDialog("Error - account not created.", "Error")


# Check if they have anything entered
def processLogin(username, password):
    db = Database.Database()

    if not username or not password:
        print("You must enter a username and password!")
        showDialog("You must enter a username and password!", "Error")
        return False
    
    # Check for valid username & password.  If EITHER are incorrect, say that EITHER are incorrect, not "user incorrect" or "pass incorrect"
    login_info = db.getLoginInfo()

    if username not in login_info.keys() or password not in login_info[username]:
        print("Username or password invalid.")
        showDialog("Username or password invalid.", "Error")
        return False
    elif username in login_info.keys() and password in login_info[username]:
        # If both valid
        db.CURRENT_USERNAME = username
        PM.CURRENT_USERNAME = username
        return True


def createProject(proj_name, proj_desc):
    db = Database.Database()

    if len(proj_name) == 0:
        print("Error - project needs a name to create it.")
        showDialog("Error - project needs a name to create it.", "Error")
        return
    else:
        idx = getID(db)
        date = datetime.now().strftime("%m/%d/%Y")
        query = """INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        values = (int(idx), str(PM.CURRENT_USERNAME), str(proj_name), str(date), "NULL", "NULL", str(proj_desc), 0, "NULL")
        insertions = {}
        insertions[values] = query
        result = db.insert(insertions)
        if result is False:
            print("Error with submitting these entries.")
            return False
        else:
            return True


def deleteProject(proj_name):
    db = Database.Database()

    query = """DELETE FROM projects WHERE project_name = ?;"""
    values = (str(proj_name),)
    result = db.delete(query, values)
    if result is False:
        print("Error with deleting file.")
        return False
    else:
        return True


def createTask(task_name, task_desc):
    pass


def createIssue(issue_name, issue_desc):
    pass


def getID(db):
    all_ids = db.getProjectIds()
    # Get a free ID slot by checking against IDs in database
    id = 1
    while True:
        if id in all_ids:
            print("ID already found in DB -- incrementing before assigning.")
            id += 1
        else:
            return id


def getFileID(db):
    all_ids = db.getFileIds()
    # Get a free ID slot by checking against IDs in database
    id = 1
    while True:
        if id in all_ids:
            print("ID already found in DB -- incrementing before assigning.")
            id += 1
        else:
            return id


def insertFile(file_name):
    db = Database.Database()

    if len(file_name) == 0:
        print("Error - file needs a name to create it.")
        showDialog("Error - file needs a name to create it.", "Error")
        return
    else:
        idx = getFileID(db)
        date = datetime.now().strftime("%m/%d/%Y")
        contents = "<Insert Code>"
        query = """INSERT INTO code_files VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
        values = (int(idx), str(PM.CURRENT_USERNAME), str(file_name), str(date), str(date), str(contents), 0, "NULL")
        insertions = {}
        insertions[values] = query
        result = db.insert(insertions)
        if result is False:
            print("Error with submitting file entry.")
            return False
        else:
            return True


def insertImportedFile(file_name, file_path, file_contents):
    """Inserts imported file"""

    db = Database.Database()

    if len(file_name) == 0:
        print("Error - file needs a name to create it.")
        showDialog("Error - file needs a name to create it.", "Error")
        return
    else:
        idx = getFileID(db)
        date = datetime.now().strftime("%m/%d/%Y")
        query = """INSERT INTO code_files VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
        values = (int(idx), str(PM.CURRENT_USERNAME), str(file_name), str(date), str(date), str(file_contents), 1, str(file_path))
        insertions = {}
        insertions[values] = query
        result = db.insert(insertions)
        if result is False:
            print("Error with submitting file entry.")
            return False
        else:
            return True


def writeToFile(path, contents):
    with open(path, "r+") as f:
        f.write(contents)


def saveFile(file_name, contents, file_info):
    choice = pag.confirm("Do you want to save your changes for this file?", "Save changes?", ["Yes", "No"])
    if choice == "Yes":
        db = Database.Database()
        date = datetime.now().strftime("%m/%d/%Y")
        query = """UPDATE code_files SET file_last_save_date = ?, file_contents = ? WHERE file_name = ?;"""
        values = (str(date), str(contents), str(file_name))
        result = db.update(query, values)

        if file_info["file_isImported"] == 1:
            writeToFile(file_info["file_path"], contents)
            print("Contents saved/overwritten to file at {}".format(file_info["file_path"]))

        if result is False:
            print("Error with updating file contents.")
            return False
        else:
            return True
    else:
        return


def deleteFile(file_name):
    choice = pag.confirm(f"Are you SURE you want to delete the SELECTED file: '{file_name}'?", "Really delete file?", ["Yes", "No"])
    if choice == "Yes":
        choice2 = pag.confirm(f"Are you REALLY sure you want to delete the SELECTED file: '{file_name}'?", "Really delete file?", ["DO IT", "No"])
        if choice2 == "DO IT":
            db = Database.Database()
            query = """DELETE FROM code_files WHERE file_name = ?;"""
            values = (str(file_name),)
            result = db.delete(query, values)
            if result is False:
                print("Error with deleting file.")
                return False
            else:
                return True
        else:
            return
    else:
        return


def showDialog(msgText, msgTitle):
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Warning)
   msgBox.setText(msgText)
   msgBox.setWindowTitle(msgTitle)
   msgBox.setStandardButtons(QMessageBox.Ok)
   #msgBox.buttonClicked.connect(msgButtonClick)
   msgBox.exec()