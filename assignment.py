import PySimpleGUI as gui
import sqlite3 as sql

db = sql.connect('assignment.db')
cursor = db.cursor()

gui.theme('DarkAmber')

windowsLoaded = 1

def loginLayout(num):
    loginLayout = [
        [gui.Text("Welcome To", key=f'welcome{num}')],
        [gui.Text("Mentors 4 Mentees", key=f'title{num}')],
        [gui.Text("Stud num or techer login: ", key=f'usernametext{num}'), gui.InputText(key=f'username{num}')],
        [gui.Text("Password: ", key=f'password_TEXT{num}'), gui.InputText(key=f'password{num}')],
        [gui.Submit("login", key=f'login{num}')]
    ]

    return loginLayout, num

menteeViewLayout = [
    [gui.Text("INSERT MENTEE LAYOUT HERE")]
]

adminViewLayout = [
    [gui.Text("Welcome "), gui.Text("", key='__adminName__', size=(10, 1))],
    [gui.Text("________________________________________")],
    [gui.Button("Register Mentee", key="__NewMentee__", size=(35, 2))],
    [gui.Button("Register Mentor", key="__NewMentor__", size=(35, 2))],
    [gui.Button("Booked Tutorials", key="__Tutorials__", size=(35, 2))],
    [gui.Button("Tutorials Report", key='__Report__', size=(35, 2))],
    [gui.Button("Exit", key='__Exit__', size=(17, 2)), gui.Button("logout", key='__logout__')]
]

newMenteeLayout = [
    [gui.Text("Add A New Mentee")],
    [gui.Text("__________________")],
    [gui.Text("Name: "), gui.InputText(key='__StudName__'), gui.Text("Grade: "), gui.InputText(key='__StudGrade__')],
    [gui.Text("Student Number: "), gui.InputText(key='__StudNum__')],
    [gui.Text("Password: "), gui.InputText(key='__InitPass__'), gui.Text("Confirm Password: "), gui.InputText(key='__PassVerify__')],
    [gui.Submit("Register Student", key='__Submit__'), gui.Button("Close", key='__Exit__')]
]


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


def menteeView(studentNum):
    studInfoQuery = f"""SELECT fname FROM Students WHERE Stud_Num == {studentNum}"""
    studInfo = cursor.execute(studInfoQuery).fetchall()
    fname = studInfo[0][0]
    Mainwindow = gui.Window(f"{fname}'s Mentee Hub", menteeViewLayout)
    while True:
        event, values = Mainwindow.read()
        if event in ('exit', gui.WIN_CLOSED):
            break


def adminView(adminUser):
    global adminViewLayout
    AdminHub = gui.Window("Admin View", adminViewLayout, finalize=True)
    AdminHub['__adminName__'].update(adminUser)
    while True:
        event, Values = AdminHub.read()
        
        if event in ('__Exit__', gui.WIN_CLOSED):
            break
        if event == "__NewMentee__":
            newMentee()
        if event == '__NewMentor__':
            newMentor()
        if event == '__logout__':
            AdminHub.close()
            login()


def newMentee():
    global newMenteeLayout

    window = gui.Window("Add New Mentee", newMenteeLayout)
    while True:
        event, Values = window.read()
        
        if event in ('__Exit__', gui.WIN_CLOSED):
            break

        if event == '__Submit__':
            name = Values['__StudName__']
            grade = Values['__StudGrade__']
            StudNum = Values['__StudNum__']
            pass1 = Values['__InitPass__']
            pass2 = Values['__PassVerify__']

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
            
        if event == '__logout__':
            window.close()
            login()


def newMentor():
    print("INSERT NEW MENTOR GUI HERE ;)")


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
#nicee
login()
