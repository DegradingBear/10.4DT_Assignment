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
    """
    This function takes two variables, subject and time, and it returns a list of mentors
    that are available at the passed time and are registered to tutor the passed subject. called
    by the find mentors function and is the 'backend' behind the search for booking mentors
    """
    #format the passed information. as the time value is "any" when not specified. this turns it into
    # an empty string that when combined with the LIKE keyword, will match with every time
    if time == "Any":
        time = ""

    #define the initial query to filter out any mentors that cant teach the specified subject
    getIDquery = f"""SELECT MentorSubjects.MentorID, Subjects.Name FROM MentorSubjects
    INNER JOIN Subjects ON MentorSubjects.SubjectID = Subjects.SubjectID
    WHERE Subjects.Name like '%{subject}%'"""

    #get the results of the query
    mentorIDresults = cursor.execute(getIDquery).fetchall()
    mentors = []
    #add all of the results to a list to be used in the next query
    for tup in mentorIDresults:
        mentors.append(tup[0])
    
    #add check if there were no results, this string wont match any mentor name and it will let the next query
    #go through without causing a sqlite3 error
    if len(mentors) == 0:
        mentors = "NO MENTORS"
    #again, seperate instance if there is only one mentor
    elif len(mentors) < 2:
        mentors = f"({mentors[0]})"
    #finally, any more than 1 mentor can be added to a tuple to be passed directly into the query (because 
    # of the brackets around a tuple, this was a happy accident that made my life a little bit easier)
    else:
        mentors = tuple(mentors)

    #define the query formatted with the information from the previous query and the time variable
    #passed to the function
    finalquery = f"""SELECT Mentors.fname, Sessions.Day, Mentors.MentorID
    FROM MentorAvailabilities
    INNER JOIN Mentors ON MentorAvailabilities.MentorID = Mentors.MentorID
    INNER JOIN Sessions ON MentorAvailabilities.SessionID = Sessions.SessionID
    WHERE Mentors.MentorID in {tuple(mentors)} AND Sessions.Day LIKE '%{time}%'"""

    #get the results of the query
    finalResults = cursor.execute(finalquery).fetchall()
    
    table = []
    tableKey = []
    #add all of the results to seperate lists, one list to be passed into a table and one dictionary as a key storing the
    #  id's of elements in the table for use in querys later
    for tup in finalResults:
        #add to the table
        table.append([tup[0], tup[1]])
        #add to the table key
        tableKey.append(tup[2])
    
    #return the list and the dictionary for use by the function that called it
    return table,tableKey


def bookTutorial(mentorID, studnum, subjectName, timeName):
    """
    This function takes variables of the student number, the mentor ID the name of the subject
    and the name of the day that a tutorial is to take place and it inserts the values into
    the tutorial table.
    """
    #a query to get the id of subject with the name given. as subjects dont have the same name, this 
    # shouldnt cause any issues, even though it could be done a little bit better by getting the ID 
    # of the subject and passing it to this function, but i want to sleep at some point this year so
    #Im not going to iron out every detail such as that one for a proof of concept :)
    getSubjectIDQuery = f"SELECT SubjectID FROM Subjects WHERE Name LIKE '%{subjectName}%'"
    #execute the query
    subjectID = cursor.execute(getSubjectIDQuery).fetchone()[0]

    #same as before, get the id of the time with the name passed to the function, could be better, but sleep
    getTimeIDQuery = f"SELECT SessionID FROM Sessions WHERE Day LIKE '%{timeName}'"
    #execute the query
    TimeID = cursor.execute(getTimeIDQuery).fetchone()[0]

    #define a query but not execute it yet, because there is an "are you sure" popup before booking it
    BookQuery = f"""INSERT INTO Tutorials (MentorID, Stud_Num, SubjectID, SessionID) VALUES ({mentorID}, {studnum}, {subjectID}, {TimeID})"""
    
    #call a pop up
    if gui.popup_yes_no("Are You Sure You Want To Book This Tutorial?") == "Yes":
        #if the popup was answered with yes, execute the booking query
        cursor.execute(BookQuery)
        #get the name of the mentor for the confirmation popup
        getMentorNameQuery = f"SELECT fname FROM Mentors WHERE MentorID = {mentorID}"
        mentorName = cursor.execute(getMentorNameQuery).fetchone()[0]
        #popup telling the user that the tutorial was booked
        gui.popup_ok(f"ok, {mentorName} was successfully Booked for a {subjectName} Tutorial on {timeName}, see you then :)")
        #update the availabilities table, updating that the time that was just booked is no longer 
        # available for this particular mentor
        updateMentorAvailabilityQuery = f"""DELETE FROM MentorAvailabilities WHERE MentorID = {mentorID} AND SessionID = {TimeID}"""
        cursor.execute(updateMentorAvailabilityQuery)
        #commit changes to the database
        db.commit()
    # if the user answer no to the are you sure popup
    else:
        #tell the user that the booking was not placed
        gui.popup_ok("Ok, The Booking Was NOT Placed :)")

    
def findMentorsView(studnum):
    """
    A function that takes the value student number and creates a gui with a layout as previously
    defined. the gui takes inputs for changing the search parameters and updates a table with
    information from the find mentors function. also calls the book mentor function when a tutorial
    session is booked
    """
    #declare global variables
    global windowsLoaded
    #get the layout and reference number from an external function
    layout, refNum = findMentorsLayout(windowsLoaded)
    #incremint windows loaded variable so that the same keys arent used again
    windowsLoaded += 1
    #initialise the window using the layout
    window = gui.Window("Find Mentors", layout)

    #loop to update and display the window
    while True:
        #get the events taken place and the values of the inputs in the gui
        event, values = window.read()
        #if the window is closed either with the cross or the exit 
        # button, break the loop and close the window
        if event in [gui.WIN_CLOSED, f'__EXIT__{refNum}']:
            window.close()
            break
        
        #if the user clicks the search button
        if event == f'__Search__{refNum}':
            #set variables to values selected in the gui
            subject = values[f'__Subject__{refNum}']
            time = values[f'__Session__{refNum}']
            #get the table to display and the table key containing id's
            #from the get mentors function
            table, tableKey = getMentors(subject, time)
            #update the table displayed with the new data
            window[f'__Tutorials__{refNum}'].update(table)
        #if the user clicks on the book button
        if event == f'__Book__{refNum}':
            #if they havent selected a tutorial in the table
            if not values[f'__Tutorials__{refNum}']:
                #tell the user to select a tutorial
                gui.popup_ok("please select a tutorial to book")
            #else if the user has slected a tutorial but hasnt specified a subject in their search
            elif not values[f'__Subject__{refNum}']:
                #tell them to specify a subject so that the mentors that they book
                # can teach the specific subject
                gui.popup("""Please Select A Subject As This Tutor 
                May Not Be Able To Tutor You In The Field That You Are Looking For""")
            #else, ie the user has specified a subject and has selected a tutorial
            else:
                #call the book tutorial function to insert the values into the booked tutorials table
                bookTutorial(tableKey[values[f'__Tutorials__{refNum}'][0]], studnum, subject,
                table[values[f'__Tutorials__{refNum}'][0]][1])


def seeTutorials(studnum):
    """
    This function creates a gui that displays all of the tutorials that the user has booked
    requires the students number for query purposes
    """
    #declare global variables
    global windowsLoaded
    #get the layout and reference number from the re-usable layout function
    layout, refNum = seeTutorialsLayout(windowsLoaded, studnum)
    #initialise the gui
    tutorialsWindow = gui.Window("My Tutorials", layout, finalize=True)
    #get all the tutorials booked from an external function. and a dictionary key containing
    # the id's for query purposes
    data, key = getTutorialsBooked(studnum)
    #update the window with the data just obtained
    tutorialsWindow[f'__Table__{refNum}'].update(data)
    #while true loop to display and update the window
    while True:
        # get the events and information information entered into the window
        event, values = tutorialsWindow.read()

        #break if the user closes the window or hits the exit button
        if event == f'__exit__{refNum}' or event == gui.WIN_CLOSED:
            break
        
        #if the user clicks the remove button
        if event == f'__REMOVE__{refNum}':
            # if the user hasnt selected anything in the table
            if not values[f'__Table__{refNum}']:
                # tell the user to select a tutorial
                gui.popup_ok("Please Select A Tutorial To Cancel")
            #if the user has selected a tutorial from the table
            else:
                # set values to the values stored in the key dictionary, for use in query
                mentorID = key['MentorID']
                sessionID = key['SessionID']
                # set a query to remove the selected tutorial
                query = f"""DELETE FROM Tutorials
                WHERE MentorID = {mentorID} AND SessionID = {sessionID}"""
                #popup to confirm the removal of the selected tutorial, if yes...
                if gui.popup_yes_no(f"Are You Sure You Want To Cancel Your {data[0][1][0]} Tutorial with {data[0][0][0]}?") == "Yes":
                    #execute the removal query
                    cursor.execute(query)
                    updateAvailabilities = f"""INSERT INTO MentorAvailabilities (MentorID, SessionID) VALUES ("{mentorID}", "{sessionID}")"""
                    cursor.execute(updateAvailabilities)
                    #save changes to the database
                    db.commit()
                    #update the information in the list and dictionary and update the table in the window
                    data, key = getTutorialsBooked(studnum)
                    tutorialsWindow[f'__Table__{refNum}'].update(data)
                else: #if the user changes their mind
                    #tell the user that the tutorial was not cancelled
                    gui.popup_ok("ok, This Tutorial Was Not Cancelled, See You Then")



def menteeView(studentNum):
    """
    this function is the window that is the 'hub' for the mentee view, it contains buttons
    to redirect to other windows that actually contain the functionality of this project
    """
    #declare global variables
    global windowsLoaded
    #get the students info using the passed student number
    studInfoQuery = f"""SELECT fname FROM Students WHERE Stud_Num == {studentNum}"""
    studInfo = cursor.execute(studInfoQuery).fetchall()
    fname = studInfo[0][0]
    #get the layout and reference number from a reusable layout function
    layout, refNum = menteeViewLayout(windowsLoaded)
    #incremint the windows loaded to avoid duplicate key errors
    windowsLoaded += 1
    #initialize the window
    Mainwindow = gui.Window(f"{fname}'s Mentee Hub", layout, finalize=True)
    #update the window to display the users name, aquired by the previous query
    Mainwindow[f'__FName__{refNum}'].update(f"{fname}'s")

    #main loop to update and display the window
    while True:
        #detect events and get values from input fields
        event, values = Mainwindow.read()
        #if the user closes the window or clicks the exit button, break the loop and close the window
        if event in [f'__Exit__{refNum}', gui.WIN_CLOSED]:
            break
        #if the user clicks the logout button, close the window and open the login window
        if event == f'__Logout__{refNum}':
            Mainwindow.close()
            login()
            break
        #if the user clicks the find mentors button, load the find mentors window
        if event == f'__FindMentor__{refNum}':
            findMentorsView(studentNum)
        #if the user clicks the my tutorials button, load the seeTutorials window function
        if event == f'__BookedTutorials__{refNum}':
            seeTutorials(studentNum)


def adminView(adminUser):
    """
    This function displays a window that is the 'hub' for the admin interface
    it contains buttons that redirect to all the other functionalities that the admin has access to
    """
    #declare global variables
    global windowsLoaded
    #get the layout and reference number from the reusable layout function
    Layout, refNum = adminViewLayout(windowsLoaded)
    #incremint the windows loaded to prevent a duplicate key error
    windowsLoaded += 1
    #initialize the window
    AdminHub = gui.Window("Admin View", Layout, finalize=True)
    #update values using the admin user value passed to the function from the login function
    AdminHub[f'__adminName__{refNum}'].update(adminUser)

    #main loop that updates and displays the window
    while True:
        #detect events and input in the window
        event, Values = AdminHub.read()
        
        #if the user closes the window or presses the exit button, break the loop
        if event in (f'__Exit__{refNum}', gui.WIN_CLOSED):
            break
        
        #if the admin clicks the new user button, call the function that displays that window
        if event == f"__NewMentee__{refNum}":
            newMentee()
        #call the new mentor function
        if event == f'__NewMentor__{refNum}':
            newMentor()
        #if the user logs out, close the window and open the login window again
        if event == f'__logout__{refNum}':
            AdminHub.close()
            login()
            break
        #if the user presses the report button, call the function that produces the report
        if event == f'__Report__{refNum}':
            Report()
        #create a new admin
        if event == f"__NewAdmin__{refNum}":
            newAdmin()


def newMentee():
    """
    This function if the window that is called by the admin page, the window that
    allows the user to create and add a new mentee to the database.
    """
    #declare global variables
    global windowsLoaded
    #get the layout and reference number from the reusable layout function
    layout, refNum = newMenteeLayout(windowsLoaded)
    # incremint the windows loaded variable to avoid the duplicate key error
    windowsLoaded += 1
    # initialize the window
    window = gui.Window("Add New Mentee", layout)
    #main loop that displays and updates the window
    while True:
        #get events and values that were inputed in the window
        event, Values = window.read()
        
        #If the user closes the window or clicks the exit button, break the loop
        if event == f'__Exit__{refNum}' or event == gui.WIN_CLOSED:
            break
        
        #if the user clicks the submit button, get values and add the mentee
        if event == f'__Submit__{refNum}':
            #get values from the inputs on the window
            name = Values[f'__StudName__{refNum}']
            grade = Values[f'__StudGrade__{refNum}']
            StudNum = Values[f'__StudNum__{refNum}']
            pass1 = Values[f'__InitPass__{refNum}']
            pass2 = Values[f'__PassVerify__{refNum}']

            #split the name variable into the first and last name
            fname, lname = nameSplit(name)

            #if the user input more than one word/name in the name field
            if fname != False:
                #if the two passwords dont match, popup to tell the user to check the inputed passwords
                if not areEqual(pass1, pass2):
                    gui.popup_ok("The Passwords Dont Match :(")
                #if the passwords do match
                else:
                    #declare query using the information gathered from the window
                    addQuery = f"""INSERT INTO Students('Stud_Num', 'Password', 'fname', 'lname', 'Grade')
                    VALUES({StudNum}, "{pass1}", "{fname}", "{lname}", {grade})"""

                    if gui.popup_yes_no(f"are you sure you want to add {fname}?"): #if the user is sure
                        #execute the query and commit changes
                        cursor.execute(addQuery)
                        db.commit()
                        #tell the user that the mentee was added
                        gui.popup_ok(f"{fname} was successfuly registered as a Mentee")
                    else: #if the user isnt sure
                        #tell the user that the mentee wasnt added
                        gui.popup_ok(f"ok, {fname} was not added :)")
                    #close the window
                    window.close()
            else: # if the user only put a one word/name string into the name fields
                #tell the user to put the full name ie, first and last name
                gui.popup_ok("Please Enter The Students Full Name")
        #if the user clicks the logout button
        if event == f'__logout__{refNum}':
            #close the window and call the login function
            window.close()
            login()
            break


def newAdmin():
    """
    This window is accesable by the admin hub, and is used to add more admin accounts to the
    database.
    """
    #declare global variables
    global windowsLoaded

    #get the layout and reference number from the reusable layout functions
    layout, refNum = newAdminLayout(windowsLoaded)
    #incremint the windows loaded variable to avoid key duplicate error
    windowsLoaded += 1
    #initialise the window
    newAdminWindow = gui.Window("Add A New Admin", layout)

    #main loop that updates and displays the window
    while True:
        #get events that occured and values that were input into the window
        event, values = newAdminWindow.read()

        #if the user closed the window or clicked the exit button, break the loop and close the window
        if event in [gui.WIN_CLOSED, f'__Exit__{refNum}']:
            newAdminWindow.close()
            break
        #if the user clicks the submit button
        if event == f'__SUBMIT__{refNum}':
            #if each of the fields have values put in them
            if values[f'__Username__{refNum}'] and values[f'__Password__{refNum}'] and values[f'__ConfirmPass__{refNum}']:
                #get the value put into the username field
                username = values[f'__Username__{refNum}']
                #if the two passwords are identical
                if areEqual(values[f'__Password__{refNum}'], values[f'__ConfirmPass__{refNum}']):
                    #define the query to add the admin
                    addQuery = f"""INSERT INTO AdminLogin (Username, Password) VALUES ("{username}", "{values[f'__Password__{refNum}']}")"""
                    #if the user is sure they want to add this admin
                    if gui.popup_yes_no(f"Are You Sure You Want To Make {username} An Admin? ") == "Yes":
                        #execute the query and commit the changes
                        cursor.execute(addQuery)
                        db.commit()
                        #tell the user that the admin was added and close the window
                        gui.popup_ok(f"ok, {username} is now an admin")
                        newAdminWindow.close()
                        break
                    else: #if the user isnt sure...
                        #dont add the admin, tell the user and close the window
                        gui.popup_ok(f"ok, {username} is not an admin")
                        newAdminWindow.close()
                        break


def newMentor():
    """
    i didnt get around to making this functionality of the app, just wanted to you know...
    sleep sometime this term :)
    """
    print("INSERT NEW MENTOR GUI HERE ;)")


def getAmount(type_):
    """
    This function returns the count of a type of user depending on the type variable that is passed to it
    """
    if type_ == "mentees":
        #query the amount of students entries
        query = """SELECT count(*)
        FROM Students"""
    elif type_ == "mentors":
        #query the amount of mentors entries
        query = """SELECT count(*)
        FROM Mentors"""
    #execute the query
    results = cursor.execute(query).fetchall()
    #return the raw number that came from the query
    return results[0][0]


def nameSplit(name):
    """
    This function splits the name passed to it from the add mentee function
    it takes the full name string and splits it into two strings, the fname and the lname
    that it returns
    """
    #split the full name into two strings
    nameList = name.split()
    #for each string in the name list
    for string in nameList: 
        if string == " ":
            nameList.remove(string) #remove the string if its empty
    try: #try returning the first and last name strings
        return nameList[0], nameList[1]
    except IndexError: #index error if there werent two strings
        return False, False #return false false, indicating that there werent two names inputed


def areEqual(a, b):
    """
    Thought of this function when i was sleep deprived. it is very redundant.  :)
    """
    #return true if the two values are equal and false if not, totally not
    # a function that litteraly emulates the == operator or anything... hehe...
    if a == b:
        return True
    else:
        return False


def getTutorialsBooked(studNum):
    """
    This function takes the variable of student number and returns the information around
    every tutorial that the student is booked in the database
    """
    #declare the query using the student number
    getTutorialsQuery = f"""SELECT Mentors.fname, Subjects.Name, Sessions.Day, Mentors.MentorID, Sessions.SessionID
    FROM Tutorials
    INNER JOIN Sessions ON Tutorials.SessionID = Sessions.SessionID
    INNER JOIN Mentors ON Tutorials.MentorID = Mentors.MentorID
    INNER JOIN Subjects ON Tutorials.SubjectID = Subjects.SubjectID
    WHERE Tutorials.Stud_Num = {studNum}"""
    #execute and fetchall the query results
    getTutorialsResults = cursor.execute(getTutorialsQuery).fetchall()
    #tutorial list, putting the information in the form that is accepted by the psg table element
    tutList = []
    #for every index of the returned results
    for tutorial in getTutorialsResults:
        tutList.append([[tutorial[0]], [tutorial[1]], [tutorial[2]]])#add the information to the table
    
    #set a dictionary with keys but no values
    raw_data = {"MentorID":None, "SessionID":None}

    for tutorial in getTutorialsResults:
        #update the raw_data dictionary
        raw_data['MentorID'] = tutorial[3]
        raw_data['SessionID'] = tutorial[4]
    return tutList, raw_data

#call the initial function
login()
