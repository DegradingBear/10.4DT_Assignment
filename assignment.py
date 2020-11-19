# import dependancies
import PySimpleGUI as gui
import sqlite3 as sql

#connect to the database
db = sql.connect('assignment.db')
cursor = db.cursor()

#set theme
gui.theme('DarkAmber')

#set global variable for loading windows several times
windowsLoaded = 1


def loginLayout(num):
    """
    this function takes a variable (num) which is passed as the number of windows loaded and it uses formatted keys with this number
    to create a layout with completely different keys but the same layout, avoiding the duplicate key error of pysimple gui
    this function returns the layout defined in it and the number to reference each of the layouts keys
    """
    #set layout
    Layout = [
        [gui.Text("Welcome To", key=f'welcome{num}')],
        [gui.Text("Mentors 4 Mentees", key=f'title{num}')],
        [gui.Text("Stud num or techer login: ", key=f'usernametext{num}'), gui.InputText(key=f'username{num}')],
        [gui.Text("Password: ", key=f'password_TEXT{num}'), gui.InputText(key=f'password{num}')],
        [gui.Submit("login", key=f'login{num}')]
    ]

    #return layout and the reference number
    return Layout, num


def seeTutorialsLayout(num, studNum):
    """
    Same reusable layout template with the same return values
    """
    #create an empty table in the format [[['fillerText'], ['fillerText'], [fillerText]], [['fillerText'], ['fillerText'], [fillerText]]]] etc
    #this is to be used as a placeholder values for the pysimple gui table
    data = [['Filler Text'for col in range(3)]for row in range(3)]

    #define layout
    layout = [
        [gui.Table(headings=["Tutor", "Subject", "Day"], values=data, key=f'__Table__{num}',def_col_width=11)],
        [gui.Button("Exit", key=f'__exit__{num}'), gui.Button("Cancel This Tutorial", key=f'__REMOVE__{num}')]
    ]
    #return values
    return layout, num


def menteeViewLayout(num):
    """
    Same as before, returns same layout with different keys
    """
    #define layout with keys formatted to the windows loaded
    menteeViewLayoutList = [
        [gui.Text("", size=(6, 1), key=f'__FName__{num}'), gui.Text("Mentors For Mentees Hub", key=f'insert{num}')],
        [gui.Button("Find Mentors", key=f'__FindMentor__{num}', size=(20,2))],
        [gui.Button("My Tutorials", key=f'__BookedTutorials__{num}', size=(20,2))],
        [gui.Button("Exit", key=f'__Exit__{num}'), gui.Button("Logout", key=f'__Logout__{num}')]
    ]

    #return values
    return menteeViewLayoutList, num


def adminViewLayout(num):
    """
    Reusable layout template function, same as before
    """
    #define layout
    Layout = [
        [gui.Text("Welcome ", key=f'welcome{num}'), gui.Text("", key=f'__adminName__{num}', size=(10, 1))],
        [gui.Text("________________________________________", key=f'divide{num}')],
        [gui.Button("Register Mentee", key=f"__NewMentee__{num}", size=(35, 2))],
        [gui.Button("Register Mentor", key=f"__NewMentor__{num}", size=(35, 2))],
        [gui.Button("Add New Admin", key=f"__NewAdmin__{num}", size=(35, 2))],
        [gui.Button("Booked Tutorials", key=f"__Tutorials__{num}", size=(35, 2))],
        [gui.Button("Tutorials Report", key=f'__Report__{num}', size=(35, 2))],
        [gui.Button("Exit", key=f'__Exit__{num}', size=(17, 2)), gui.Button("logout", key=f'__logout__{num}', size=(17, 2))]
    ]
    #return values
    return Layout, num


def newMenteeLayout(num):
    """
    Reusable Layout
    """
    newMenteeLayout = [
        [gui.Text("Add A New Mentee", key=f'title{num}')],
        [gui.Text("__________________", key=f'Barrier{num}')],
        [gui.Text("Name: ", key=f'NamePrompt{num}'), gui.InputText(key=f'__StudName__{num}'),
        gui.Text("Grade: ", key=f'grade Prompt {num}'), gui.InputText(key=f'__StudGrade__{num}')],
        [gui.Text("Student Number: ", key=f'studnumprompt{num}'), gui.InputText(key=f'__StudNum__{num}')],
        [gui.Text("Password: ", key=f'passPrompt{num}'), gui.InputText(key=f'__InitPass__{num}'),
        gui.Text("Confirm Password: ", key=f'confirmPrompt{num}'), gui.InputText(key=f'__PassVerify__{num}')],
        [gui.Submit("Register Student", key=f'__Submit__{num}'), gui.Button("Close", key=f'__Exit__{num}')]
    ]

    #reuturn values
    return newMenteeLayout, num


def reportLayout(num):
    """
    Reusable layout function
    """
    data = [['' for row in range(2)]for col in range(6)]
    layout = [
        [gui.Text("Total Tutorials: ", key=f'totutexp{num}'), gui.Text("", key=f'__TotalTutorials__{num}', size=(6,1))],
        [gui.Table(values=data, headings=["     Subject     ", "Total Tutorials"], key=f'__SubjAmount__{num}')],
        [gui.Text("Mentees: ", key=f'menteesPoint{num}'), gui.Text("", key=f'Num__Mentees__{num}', size=(5,0)),
        gui.Text("Mentors: ", key=f'mentorsPoint{num}'), gui.Text("", key=f'Num__Mentors__{num}', size=(5,0))]
    ]

    #return values
    return layout, num


def findMentorsLayout(num):
    """
    this function returns a layout just like the others but obtains some data from the database to use in the layout
    before returning the layout.
    """

    #get the name of every subject and add it to a list
    #this list is used for a dropBox selection when filtering mentors by subjects they teach
    Subquery = """SELECT Name FROM Subjects"""
    Subresults = cursor.execute(Subquery).fetchall()
    subjectsList = []
    for tup in Subresults:
        subjectsList.append(tup[0])

    #same as before but returning the name of days/sessions
    timeQuery = """SELECT Day FROM Sessions"""
    timeResults = cursor.execute(timeQuery).fetchall()
    timeList = ["Any"]
    for tup in timeResults:
        timeList.append(tup[0])

    #filler values for the py simple gui table element, replaced later on, when search button clicked
    data = [['           ' for row in range(2)]for col in range(6)]
    #define layout using data just obtained
    layout = [
        [gui.Text("Subject: ", key=f'SubjectPrompt{num}'), gui.Combo(subjectsList, key=f'__Subject__{num}')],
        [gui.Text("Session", key=f'SessionPrompt{num}'), gui.Combo(timeList, key=f'__Session__{num}')],
        [gui.Submit("Update Tutorials", key=f'__Search__{num}'), gui.Button("Exit", key=f'__EXIT__{num}')],
        [gui.Table(headings=['Mentor', 'Session'], values=data, key=f'__Tutorials__{num}', size=(20, None))],
        [gui.Button("Book Selected Tutorials", key=f'__Book__{num}')]
    ]
    #returning the layout and reference number for the keys
    return layout, num


def  newAdminLayout(num):
    """
    this is another reusable layout function
    """
    #define layout
    layout = [
        [gui.Text("Username: ", key=f'__UsernamePrompt__{num}'), gui.InputText(default_text="username", key=f'__Username__{num}')],
        [gui.Text("Password: ", key=f'__PasswordPrompt__{num}'), gui.InputText(default_text="password", key=f'__Password__{num}'),
        gui.Text("Confirm Password: ", key=f'__ConfirmPasswordPrompt__{num}'),
        gui.InputText(default_text="confirm password", key=f'__ConfirmPass__{num}')],
        [gui.Submit("Add Admin", key=f'__SUBMIT__{num}'), gui.Button("Cancel", key=f'__Exit__{num}')]
    ]
    #return values
    return layout, num


def Report():
    """
    This function is the window for the report that admins can view. it uses a while true loop to update
    a psg window untill closed and it displays information on the number of mentors, mentees, tutorials, etc
    """
    #declare global windows loaded so that the key for the reusable layout will  differ each time
    global windowsLoaded

    #get the layout and reference number from one of the defined reusable layout functions
    layout, refNum = reportLayout(windowsLoaded)
    #incremint the number of windows loaded so that the next time the layout is called, it will definately have differing keys
    windowsLoaded += 1
    #declare the window
    report = gui.Window("Tutorials Report", layout, finalize=True)

    #update each of the elements with data from seperate funtions
    report[f'__SubjAmount__{refNum}'].update(getSubjectsList())
    report[f'Num__Mentees__{refNum}'].update(getAmount("mentees"))
    report[f'Num__Mentors__{refNum}'].update(getAmount("mentors"))
    report[f'__TotalTutorials__{refNum}'].update(getTotalTut())

    #loop to open the window
    while True:
        #get events and values
        event, values = report.read()
        #break if the event is to exit the window
        if event in [f'__EXIT__{refNum}', gui.WIN_CLOSED]:
            break


def getTotalTut():
    """
    This function returns the total number of tutorials that have been booked, referenced in the report window
    is simple, just moved to a seperate function to clear up clutter and make the actual window functions relatively
    clean
    """

    #define a multi-line string as a query, to be executed
    query = """SELECT count(*)
    FROM Tutorials"""

    #execute the query and fetchall
    result = cursor.execute(query).fetchall()

    #return the result of the query, which will be the total number of tutorials booked
    return result[0][0]


def getSubjectsList():
    """
    this query generates nested lists in the psg table format that displays the name of the subject and
    the number of tutorials booked for this subject. called by the report function
    """

    #define the query
    query = """SELECT Subjects.Name, count(*)
    FROM Tutorials
    INNER JOIN Subjects ON Tutorials.SubjectID = Subjects.SubjectID
    GROUP BY Tutorials.SubjectID"""

    #get results
    result = cursor.execute(query).fetchall()
    #declare the return table as an empty list
    data = []

    #repeat the following code for each entry in the database that was returned with the previous query
    for tup in result:
        #declare a row
        row = []
        #add the subject name as a column to the row
        row.append([str(tup[0])])
        #add the count of tutorials as a column to the row
        row.append([str(tup[1])])
        #add the row to the data table
        data.append(row)
    
    #return the table formatted list
    return data


def QueryLogin(username, password):
    """
    This function takes two variables from the login window, the username and the password. it then executes a query
    to find any account first in students then if there is none in students, it checks admins. this query returns the id and the
    usertype of the account with credentials that match the username and password passed to it, called by the login function
    """

    #define the queries
    StudLoginQuery = f"""SELECT Password, fname
    FROM Students WHERE Stud_Num == "{username}" """

    adminLoginQuery = f"""SELECT Password
    FROM AdminLogin WHERE Username == "{username}" """

    #execute the student search query
    studResults = cursor.execute(StudLoginQuery).fetchall()

    #if no data was returned by the student query
    if not studResults:
        #check the admin table
        adminResults = cursor.execute(adminLoginQuery).fetchall()
        #if there were no matches in the admin table
        if not adminResults:
            #make the validity of the login attempt false, this is used to only check the other elements that
            #should be in the dictionary if there are matches or if the validility is true, this method avoids index errors
            return {'valid': False}
        else:
            #if the credentials were in the admin table, make the validity of the login attempt true and return the user details
            return {'valid': True, 'password': adminResults[0][0], 'name': "admin"}
    else:
        #if the credentials were in the students table, make the validity of the login attempt true and return the user details
        return {'valid': True, 'password': studResults[0][0], 'name': studResults[0][1]}


def login():
    """
    This is a window function that uses a layout that was previously declared
    it shows a login window and if the user tries to login, it calls the querylogin function
    if the queryLogin function returns valid, it redirects to the respective page of each user and if not
    it has a popup that tells the user that they used an incorrect username or password
    """

    #declare global variables
    global cursor, user, windowsLoaded
    #get the layout and reference number from a reusable layout function
    login, refNum = loginLayout(windowsLoaded)
    #incremint the number of windows loaded so that the same layout keys are never used
    windowsLoaded += 1
    #initialise the window
    window = gui.Window("M 4 M", login)

    #loop to show the window
    while True:
        #read the input and events from the login window
        event, values = window.read()
        #break if the window is closed
        if event == gui.WIN_CLOSED:
            break
        #if the user clicks the login button
        if event == f'login{refNum}':
            #get values from the input feilds
            username = values[f'username{refNum}']
            password = values[f'password{refNum}']

            #call the query login function to check if the inputed username and password are valid
            result = QueryLogin(username, password)

            #check if the credentials actually returned result, so as to avoid an index error when checking further on
            if result['valid']:
                #set a variable as the correct password
                correctPass = result['password']
                #set the username/name of the user from the query aswell
                fname = result['name']
                #if the password matches the one in the database
                if password == correctPass:
                    #login
                    gui.popup_ok(f"logged in as {fname}")
                    #check if the user is an admin
                    if fname == "admin":
                        #close the window and login as an admin
                        window.close()
                        adminView(username)
                    else: # if the user is a mentee (not an admin)
                        #close the login window and open the mentee view using the username of the mentee
                        #ie the student number
                        window.close()
                        menteeView(username)
                else: #if the password given did not match the correct password
                    #tell the user
                    gui.popup_ok("Incorrect Username Or Password")
            else: # if the username given isnt in the database
                #tell the user
                gui.popup_ok("Incorrect Username or Password")


def getMentors(subject, time):
    if time == "Any":
        time = ""

    getIDquery = f"""SELECT MentorSubjects.MentorID, Subjects.Name FROM MentorSubjects
    INNER JOIN Subjects ON MentorSubjects.SubjectID = Subjects.SubjectID
    WHERE Subjects.Name like '%{subject}%'"""

    mentorIDresults = cursor.execute(getIDquery).fetchall()
    mentors = []
    for tup in mentorIDresults:
        mentors.append(tup[0])
    
    if len(mentors) == 0:
        mentors = "NO MENTORS"
    elif len(mentors) < 2:
        mentors = f"({mentors[0]})"
    else:
        mentors = tuple(mentors)

    finalquery = f"""SELECT Mentors.fname, Sessions.Day, Mentors.MentorID
    FROM MentorAvailabilities
    INNER JOIN Mentors ON MentorAvailabilities.MentorID = Mentors.MentorID
    INNER JOIN Sessions ON MentorAvailabilities.SessionID = Sessions.SessionID
    WHERE Mentors.MentorID in {tuple(mentors)} AND Sessions.Day LIKE '%{time}%'"""

    finalResults = cursor.execute(finalquery).fetchall()
    
    table = []
    tableKey = []
    for tup in finalResults:
        table.append([tup[0], tup[1]])
        tableKey.append(tup[2])
    
    return table,tableKey


def bookTutorial(mentorID, studnum, subjectName, timeName):
    getSubjectIDQuery = f"SELECT SubjectID FROM Subjects WHERE Name LIKE '%{subjectName}%'"
    subjectID = cursor.execute(getSubjectIDQuery).fetchone()[0]

    getTimeIDQuery = f"SELECT SessionID FROM Sessions WHERE Day LIKE '%{timeName}'"
    TimeID = cursor.execute(getTimeIDQuery).fetchone()[0]

    BookQuery = f"""INSERT INTO Tutorials (MentorID, Stud_Num, SubjectID, SessionID) VALUES ({mentorID}, {studnum}, {subjectID}, {TimeID})"""
    
    if gui.popup_yes_no("Are You Sure You Want To Book This Tutorial?") == "Yes":
        cursor.execute(BookQuery)
        getMentorNameQuery = f"SELECT fname FROM Mentors WHERE MentorID = {mentorID}"
        mentorName = cursor.execute(getMentorNameQuery).fetchone()[0]
        gui.popup_ok(f"ok, {mentorName} was successfully Booked for a {subjectName} Tutorial on {timeName}, see you then :)")
        updateMentorAvailabilityQuery = f"""DELETE FROM MentorAvailabilities WHERE MentorID = {mentorID} AND SessionID = {TimeID}"""
        cursor.execute(updateMentorAvailabilityQuery)
        db.commit()
    else:
        gui.popup_ok("Ok, The Booking Was NOT Placed :)")

    
def findMentorsView(studnum):
    global windowsLoaded
    layout, refNum = findMentorsLayout(windowsLoaded)
    windowsLoaded += 1
    window = gui.Window("Find Mentors", layout)

    while True:
        event, values = window.read()
        if event in [gui.WIN_CLOSED, f'__EXIT__{refNum}']:
            window.close()
            break
        if event == f'__Search__{refNum}':
            subject = values[f'__Subject__{refNum}']
            time = values[f'__Session__{refNum}']
            table, tableKey = getMentors(subject, time)
            window[f'__Tutorials__{refNum}'].update(table)
        if event == f'__Book__{refNum}':
            if not values[f'__Tutorials__{refNum}']:
                gui.popup_ok("please select a tutorial to book")
            elif not values[f'__Subject__{refNum}']:
                gui.popup("Please Select A Subject As This Tutor May Not Be Able To Tutor You In The Field That You Are Looking For")
            else:
                bookTutorial(tableKey[values[f'__Tutorials__{refNum}'][0]], studnum, subject, table[values[f'__Tutorials__{refNum}'][0]][1])


def seeTutorials(studnum):
    global windowsLoaded
    layout, refNum = seeTutorialsLayout(windowsLoaded, studnum)

    tutorialsWindow = gui.Window("My Tutorials", layout, finalize=True)
    data, key = getTutorialsBooked(studnum)
    tutorialsWindow[f'__Table__{refNum}'].update(data)
    while True:
        event, values = tutorialsWindow.read()

        if event == f'__exit__{refNum}' or event == gui.WIN_CLOSED:
            break

        if event == f'__REMOVE__{refNum}':
            if not values[f'__Table__{refNum}']:
                gui.popup_ok("Please Select A Tutorial To Cancel")
            else:
                mentorID = key['MentorID']
                sessionID = key['SessionID']
                query = f"""DELETE FROM Tutorials WHERE MentorID = {mentorID} AND SessionID = {sessionID}"""
                if gui.popup_yes_no(f"Are You Sure You Want To Cancel Your {data[0][1][0]} Tutorial with {data[0][0][0]}?") == "Yes":
                    cursor.execute(query)
                    db.commit()
                    data, key = getTutorialsBooked(studnum)
                    tutorialsWindow[f'__Table__{refNum}'].update(data)
                else:
                    gui.popup_ok("ok, This Tutorial Was Not Cancelled, See You Then")



def menteeView(studentNum):
    global windowsLoaded
    studInfoQuery = f"""SELECT fname FROM Students WHERE Stud_Num == {studentNum}"""
    studInfo = cursor.execute(studInfoQuery).fetchall()
    fname = studInfo[0][0]
    layout, refNum = menteeViewLayout(windowsLoaded)
    windowsLoaded += 1
    Mainwindow = gui.Window(f"{fname}'s Mentee Hub", layout, finalize=True)
    Mainwindow[f'__FName__{refNum}'].update(f"{fname}'s")

    while True:
        event, values = Mainwindow.read()
        if event in [f'__Exit__{refNum}', gui.WIN_CLOSED]:
            break
        if event == f'__Logout__{refNum}':
            Mainwindow.close()
            login()
        if event == f'__FindMentor__{refNum}':
            findMentorsView(studentNum)
        if event == f'__BookedTutorials__{refNum}':
            seeTutorials(studentNum)


def adminView(adminUser):
    global windowsLoaded
    Layout, refNum = adminViewLayout(windowsLoaded)
    windowsLoaded += 1
    AdminHub = gui.Window("Admin View", Layout, finalize=True)
    AdminHub[f'__adminName__{refNum}'].update(adminUser)

    while True:
        event, Values = AdminHub.read()
        
        if event in (f'__Exit__{refNum}', gui.WIN_CLOSED):
            break
        if event == f"__NewMentee__{refNum}":
            newMentee()
        if event == f'__NewMentor__{refNum}':
            newMentor()
        if event == f'__logout__{refNum}':
            AdminHub.close()
            login()
        if event == f'__Report__{refNum}':
            Report()
        if event == f"__NewAdmin__{refNum}":
            newAdmin()


def newMentee():
    global windowsLoaded
    layout, refNum = newMenteeLayout(windowsLoaded)
    windowsLoaded += 1
    window = gui.Window("Add New Mentee", layout)
    while True:
        event, Values = window.read()
        
        if event == f'__Exit__{refNum}' or event == gui.WIN_CLOSED:
            break

        if event == f'__Submit__{refNum}':
            name = Values[f'__StudName__{refNum}']
            grade = Values[f'__StudGrade__{refNum}']
            StudNum = Values[f'__StudNum__{refNum}']
            pass1 = Values[f'__InitPass__{refNum}']
            pass2 = Values[f'__PassVerify__{refNum}']

            fname, lname = nameSplit(name)

            if fname != False:

                if not areEqual(pass1, pass2):
                    gui.popup_ok("The Passwords Dont Match :(")
                else:
                    addQuery = f"""INSERT INTO Students('Stud_Num', 'Password', 'fname', 'lname', 'Grade')
                    VALUES({StudNum}, "{pass1}", "{fname}", "{lname}", {grade})"""

                    cursor.execute(addQuery)
                    if gui.popup_yes_no(f"are you sure you want to add {fname}?"):
                        db.commit()
                        gui.popup_ok(f"{fname} was successfuly registered as a Mentee")
                    else:
                        gui.popup_ok(f"ok, {fname} was not added :)")
                    window.close()
            else:
                gui.popup_ok("Please Enter The Students Full Name")
            
        if event == f'__logout__{refNum}':
            window.close()
            login()


def newAdmin():
    global windowsLoaded

    layout, refNum = newAdminLayout(windowsLoaded)
    windowsLoaded += 1
    newAdminWindow = gui.Window("Add A New Admin", layout)

    while True:
        event, values = newAdminWindow.read()

        if event in [gui.WIN_CLOSED, f'__Exit__{refNum}']:
            newAdminWindow.close()
            break
        if event == f'__SUBMIT__{refNum}':
            if values[f'__Username__{refNum}'] and values[f'__Password__{refNum}'] and values[f'__ConfirmPass__{refNum}']:
                username = values[f'__Username__{refNum}']
                if areEqual(values[f'__Password__{refNum}'], values[f'__ConfirmPass__{refNum}']):
                    addQuery = f"""INSERT INTO AdminLogin (Username, Password) VALUES ("{username}", "{values[f'__Password__{refNum}']}")"""
                    if gui.popup_yes_no(f"Are You Sure You Want To Make {username} An Admin? ") == "Yes":
                        cursor.execute(addQuery)
                        db.commit()
                        gui.popup_ok(f"ok, {username} is now an admin")
                        newAdminWindow.close()
                        break
                    else:
                        gui.popup_ok(f"ok, {username} is not an admin")
                        newAdminWindow.close()
                        break


def newMentor():
    print("INSERT NEW MENTOR GUI HERE ;)")


def getAmount(type_):

    if type_ == "mentees":
        query = """SELECT count(*)
        FROM Students"""
    elif type_ == "mentors":
        query = """SELECT count(*)
        FROM Mentors"""
    results = cursor.execute(query).fetchall()

    return results[0][0]


def nameSplit(name):
    nameList = name.split()
    print(nameList)
    for string in nameList: 
        if string == " ":
            nameList.remove(string)
    try:
        return nameList[0], nameList[1]
    except IndexError:
        return False, False


def areEqual(a, b):
    if a == b:
        return True
    else:
        return False


def getTutorialsBooked(studNum):
    getTutorialsQuery = f"""SELECT Mentors.fname, Subjects.Name, Sessions.Day, Mentors.MentorID, Sessions.SessionID
    FROM Tutorials
    INNER JOIN Sessions ON Tutorials.SessionID = Sessions.SessionID
    INNER JOIN Mentors ON Tutorials.MentorID = Mentors.MentorID
    INNER JOIN Subjects ON Tutorials.SubjectID = Subjects.SubjectID
    WHERE Tutorials.Stud_Num = {studNum}"""
    getTutorialsResults = cursor.execute(getTutorialsQuery).fetchall()
    tutList = []
    for tutorial in getTutorialsResults:
        tutList.append([[tutorial[0]], [tutorial[1]], [tutorial[2]]])
    
    raw_data = {"MentorID":None, "SessionID":None}

    for tutorial in getTutorialsResults:
        raw_data['MentorID'] = tutorial[3]
        raw_data['SessionID'] = tutorial[4]
    return tutList, raw_data


login()
