import PySimpleGUI as gui
import sqlite3 as sql

db = sql.connect('assignment.db')
cursor = db.cursor()

gui.theme('DarkAmber')

windowsLoaded = 1


def loginLayout(num):
    Layout = [
        [gui.Text("Welcome To", key=f'welcome{num}')],
        [gui.Text("Mentors 4 Mentees", key=f'title{num}')],
        [gui.Text("Stud num or techer login: ", key=f'usernametext{num}'), gui.InputText(key=f'username{num}')],
        [gui.Text("Password: ", key=f'password_TEXT{num}'), gui.InputText(key=f'password{num}')],
        [gui.Submit("login", key=f'login{num}')]
    ]

    return Layout, num


def menteeViewLayout(num):
    menteeViewLayoutList = [
        [gui.Text("", size=(6, 1), key=f'__FName__{num}'), gui.Text("Mentors For Mentees Hub", key=f'insert{num}')],
        [gui.Button("Find Mentors", key=f'__FindMentor__{num}', size=(20,2))],
        [gui.Button("Exit", key=f'__Exit__{num}'), gui.Button("Logout", key=f'__Logout__{num}')]
    ]

    return menteeViewLayoutList, num


def adminViewLayout(num):
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

    return Layout, num


def newMenteeLayout(num):
    newMenteeLayout = [
        [gui.Text("Add A New Mentee", key=f'title{num}')],
        [gui.Text("__________________", key=f'Barrier{num}')],
        [gui.Text("Name: ", key=f'NamePrompt{num}'), gui.InputText(key=f'__StudName__{num}'), gui.Text("Grade: ", key=f'grade Prompt {num}'), gui.InputText(key=f'__StudGrade__{num}')],
        [gui.Text("Student Number: ", key=f'studnumprompt{num}'), gui.InputText(key=f'__StudNum__{num}')],
        [gui.Text("Password: ", key=f'passPrompt{num}'), gui.InputText(key=f'__InitPass__{num}'), gui.Text("Confirm Password: ", key=f'confirmPrompt{num}'), gui.InputText(key=f'__PassVerify__{num}')],
        [gui.Submit("Register Student", key=f'__Submit__{num}'), gui.Button("Close", key=f'__Exit__{num}')]
    ]

    return newMenteeLayout, num


def reportLayout(num):

    data = [['' for row in range(2)]for col in range(6)]
    layout = [
        [gui.Text("Total Tutorials: ", key=f'totutexp{num}'), gui.Text("", key=f'__TotalTutorials__{num}', size=(6,1))],
        [gui.Table(values=data, headings=["     Subject     ", "Total Tutorials"], key=f'__SubjAmount__{num}')],
        [gui.Text("Mentees: ", key=f'menteesPoint{num}'), gui.Text("", key=f'Num__Mentees__{num}', size=(5,0)), gui.Text("Mentors: ", key=f'mentorsPoint{num}'), gui.Text("", key=f'Num__Mentors__{num}', size=(5,0))]
    ]

    return layout, num


def findMentorsLayout(num):

    Subquery = """SELECT Name FROM Subjects"""
    Subresults = cursor.execute(Subquery).fetchall()
    subjectsList = []
    for tup in Subresults:
        subjectsList.append(tup[0])

    timeQuery = """SELECT Day FROM Sessions"""
    timeResults = cursor.execute(timeQuery).fetchall()
    timeList = ["Any"]
    for tup in timeResults:
        timeList.append(tup[0])

    data = [['' for row in range(2)]for col in range(6)]

    layout = [
        [gui.Text("Subject: ", key=f'SubjectPrompt{num}'), gui.Combo(subjectsList, key=f'__Subject__{num}')],
        [gui.Text("Session", key=f'SessionPrompt{num}'), gui.Combo(timeList, key=f'__Session__{num}')],
        [gui.Submit("Update Tutorials", key=f'__Search__{num}'), gui.Button("Exit", key=f'__EXIT__{num}')],
        [gui.Table(headings=['Mentor', 'Session'], values=data, key=f'__Tutorials__{num}', size=(20, None))],
        [gui.Button("Book Selected Tutorials", key=f'__Book__{num}')]
    ]

    return layout, num


def  newAdminLayout(num):
    layout = [
        [gui.Text("Username: ", key=f'__UsernamePrompt__{num}'), gui.InputText(default_text="username", key=f'__Username__{num}')],
        [gui.Text("Password: ", key=f'__PasswordPrompt__{num}'), gui.InputText(default_text="password", key=f'__Password__{num}'), gui.Text("Confirm Password: ", key=f'__ConfirmPasswordPrompt__{num}'), gui.InputText(default_text="confirm password", key=f'__ConfirmPass__{num}')],
        [gui.Submit("Add Admin", key=f'__SUBMIT__{num}'), gui.Button("Cancel", key=f'__Exit__{num}')]
    ]

    return layout, num


def Report():
    global windowsLoaded

    layout, refNum = reportLayout(windowsLoaded)
    windowsLoaded += 1
    report = gui.Window("Tutorials Report", layout, finalize=True)

    report[f'__SubjAmount__{refNum}'].update(getSubjectsList())
    report[f'Num__Mentees__{refNum}'].update(getAmount("mentees"))
    report[f'Num__Mentors__{refNum}'].update(getAmount("mentors"))
    report[f'__TotalTutorials__{refNum}'].update(getTotalTut())

    while True:
        event, values = report.read()

        if event in [f'__EXIT__{refNum}', gui.WIN_CLOSED]:
            break


def getTotalTut():
    query = """SELECT count(*)
    FROM Tutorials"""

    result = cursor.execute(query).fetchall()

    return result[0][0]


def getSubjectsList():
    query = """SELECT Subjects.Name, count(*)
    FROM Tutorials
    INNER JOIN Subjects ON Tutorials.SubjectID = Subjects.SubjectID
    GROUP BY Tutorials.SubjectID"""

    result = cursor.execute(query).fetchall()

    data = []

    for tup in result:
        row = []
        row.append([str(tup[0])])
        row.append([str(tup[1])])
        data.append(row)
    
    return data


def QueryLogin(username, password):
    StudLoginQuery = f"""SELECT Password, fname
    FROM Students WHERE Stud_Num == "{username}" """

    adminLoginQuery = f"""SELECT Password
    FROM AdminLogin WHERE Username == "{username}" """

    studResults = cursor.execute(StudLoginQuery).fetchall()
    if not studResults:
        adminResults = cursor.execute(adminLoginQuery).fetchall()
        if not adminResults:
            return {'valid': False}
        else:
            return {'valid': True, 'password': adminResults[0][0], 'name': "admin"}
    else:
        return {'valid': True, 'password': studResults[0][0], 'name': studResults[0][1]}


def login():
    global cursor, user, windowsLoaded
    login, refNum = loginLayout(windowsLoaded)
    windowsLoaded += 1
    window = gui.Window("M 4 M", login)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break
        if event == f'login{refNum}':
            username = values[f'username{refNum}'] #lmao
            password = values[f'password{refNum}']

            result = QueryLogin(username, password)

            if result['valid']:
                correctPass = result['password']
                fname = result['name']
                if password == correctPass:
                    gui.popup_ok(f"logged in as {fname}")
                    if fname == "admin":
                        window.close()
                        adminView(username)
                    else:
                        window.close()
                        menteeView(username)
                else:
                    gui.popup_ok("Incorrect Username Or Password")
            else:
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


login()
