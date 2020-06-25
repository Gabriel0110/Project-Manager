import Database
from datetime import datetime

import project_manager as PM

# Process account creation
def processCreation(user, pw, email):
    db = Database.Database()

    for item in [user, pw, email]:
        if not item:
            print("Username, password, and email are required!")
            return
        
    login_info = db.getLoginInfo()
    if user in login_info.keys():
        print("Username already taken.")
        return
    elif any(email in val for val in login_info.values()):
        print("Email already in use.")
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
            return True
        else:
            print("Error with account creation.")


# Check if they have anything entered
def processLogin(username, password):
    db = Database.Database()

    if not username or not password:
        print("You must enter a username and password!")
        #MainApp.createAlert(self, "You must enter a username and password.", "Error", "OK")
        return False
    
    # Check for valid username & password.  If EITHER are incorrect, say that EITHER are incorrect, not "user incorrect" or "pass incorrect"
    login_info = db.getLoginInfo()

    if username not in login_info.keys() or password not in login_info[username]:
        print("Username or password invalid.")
        return False
        #MainApp.createAlert(self, "Username or password invalid.", "Error", "OK")
    elif username in login_info.keys() and password in login_info[username]:
        # If both valid
        #MainApp.createAlert(self, "Login successful!", "Success!", "OK")
        db.CURRENT_USERNAME = username
        PM.CURRENT_USERNAME = username
        return True