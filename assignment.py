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

    query = """SELECT Name FROM Subjects"""
    results = cursor.execute(query).fetchall()
    subjectsList = []
    for tup in results:
        subjectsList.append(tup[0])

    layout = [
        [gui.Text("Subject: ", key=f'SubjectPrompt{num}'), gui.Combo(subjectsList, key=f'__Subject__{num}')]
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



def findMentorsView(studnum):
    global windowsLoaded
    layout, refNum = findMentorsLayout(windowsLoaded)
    windowsLoaded += 1
    window = gui.Window("Find Mentors", layout)

    while True:
        event, values = window.read()

        if event == gui.WIN_CLOSED:
            break


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
        if event in (f'__Exit__{refNum}', gui.WIN_CLOSED):
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

                if pass1 != pass2:
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

login()
