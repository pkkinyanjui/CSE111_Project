import sqlite3
import random
import string
from sqlite3 import Error
import PySimpleGUI as sg


def openConnection(_dbFile):
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
        print()
    except Error as e:
        print(e)

    return conn

def closeConnection(_conn, _dbFile):
  
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

def insertCar(_conn,temp):
    try:
        
        sql = """INSERT INTO Car(c_plate, c_vin, c_title, c_model, c_ownerkey) VALUES(?, ?, ?, ?, ?)"""
        
        args = temp,
        
        _conn.executemany(sql,args)

        _conn.commit()

    except Error as e:
        _conn.rollback()
        print(e)

def insertOwner(_conn,temp):


    try:
        
        sql = """INSERT INTO Owner(o_name, o_ownerkey, o_state, o_plate) VALUES( ?, ?, ?, ?)"""
        
        args = temp,
        
        _conn.executemany(sql,args)

        _conn.commit()

    except Error as e:
        _conn.rollback()
        print(e)

def insertInsurance(_conn,insuranceKey,insuranceName):
    try:
        
        sql = """INSERT INTO Insurance(i_insurancekey, i_insurancename) VALUES(?, ?)"""
         
        args = [insuranceKey,insuranceName],
        
        _conn.executemany(sql,args)

        _conn.commit()

    except Error as e:
        _conn.rollback()
        print(e)

def insertCollision(_conn, temp):
    try:
        sql = """INSERT INTO Collision(n_name1, n_name2, n_collisionkey, n_location, n_date, n_damages,n_collisiontype, n_casualty, n_insurancekey1, n_insurancekey2, n_companykey,n_statekey) VALUES(?,?,?, ? , ?, ?, ?, ?,?,?,?,?)"""
        args = temp,
        _conn.executemany(sql,args)
        _conn.commit()

    except Error as e:
        _conn.rollback()
        print(e)

##############################################
#^^^^^^^^^^ SQLITE FUNCTIONS ^^^^^^^^^^^^^^^^^
##############################################

##############################################
#vvvvvvvvvvvvvv GUI FUNCTIONS vvvvvvvvvvvvvv
##############################################

def runGUI(_conn, _dbFile):


        sg.theme('BrightColors')
        layout = [
            [sg.Text('ROAD TRAFFIC DATABASE')],
            [sg.Image('homepage.PNG')],
            [sg.Button("Upload Data", key="upload")],
            [sg.Button("View Tips", key="tips")],
            [sg.Button("View Accidents", key="accidents")],
            [sg.Button("View Insurance Coverage", key="insurance")]
        ]
        window = sg.Window("Main Window", layout, margins=(150,250))
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            if event == "tips":
                open_Tips(_conn, _dbFile)
            if event == "accidents":
                open_Spec(_conn, _dbFile)
            if event == "insurance":
                open_insurance(_conn, _dbFile)
            if event == "upload":
                open_Upload(_conn, _dbFile)
            
        window.close()

def open_Upload(_conn, _dbFile):
    layout = [
    
    [sg.Image('clip.PNG'),sg.Image('profile.PNG')],
    [sg.Button("Report Accident", key="report"),
    sg.pin(sg.Button("Upload Personal Data", key="personal"))],
    [sg.Button('Exit')]

    ]
    window = sg.Window("Second Window", layout, margins=(100,200),modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "report":
                open_Report(_conn, _dbFile)    
        if event == "personal":
                open_Personal(_conn, _dbFile)    
        
    window.close()

def open_Personal(_conn, _dbFile):
    layout = [
        [sg.Image("profile.PNG")],
        [sg.Text("Personal Data Upload", key="report")],
        [sg.Text("Please enter your data:")],
        [sg.Text('Name', size =(15, 1)), sg.InputText()],
        [sg.Text('State', size =(15, 1)), sg.InputText()],
        [sg.Text('Plate', size =(15, 1)), sg.InputText()],
        [sg.Text('Vin', size =(15, 1)), sg.InputText()],
        [sg.Text('Title', size =(15, 1)), sg.InputText()],
        [sg.Text('Model', size =(15, 1)), sg.InputText()],
        [sg.Submit('Insert')],
        [sg.Submit('Remove')],
        [sg.Button('Exit')]
    ]
    window = sg.Window("Personal Data Upload", layout, margins=(100,200),modal=True)
    choice = None
    
    while True:
        event, values = window.read()
        c = _conn.cursor()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Insert":
            temp = [0] * 4
            temp2 = [0] * 5
            
            temp[0] = values[1]
            temp[1] = "3j"
            temp[2] = values[2]
            temp[3] = values[3]
            temp2[0] = values[3]
            temp2[1] = values[4]
            temp2[2] = values[5]
            temp2[3] = values[6]
            temp2[4] = "3j"
          
            c.execute("""INSERT INTO Owner(o_name, o_ownerkey, o_state, o_plate)
            VALUES (?,?,?,?)""",(temp[0], temp[1], temp[2], temp[3]))
            c.execute("""INSERT INTO Car(c_plate, c_vin, c_title, c_model, c_ownerkey) VALUES(?, ?, ?, ?, ?)""", (temp2[0],temp2[1],temp2[2],temp2[3],temp2[4]))
            _conn.commit()
        if event == "Remove":
            temp = values[3]
            c.execute(f"""DELETE FROM Owner WHERE o_plate = 
            '{temp}'""")
            c.execute(f"""DELETE FROM Car WHERE c_plate = 
            '{temp}'""")
            _conn.commit()
        
    window.close()

def open_Report(_conn, _dbFile):
        layout = [
            [sg.Image("clip.PNG")],
            [sg.Text("Report Accident", key="report")],
            [sg.Text("Please enter details of the crash:")],
            [sg.Text('Name 1 ', size =(15, 1)), sg.InputText()
            ,sg.Text('Name 2 ', size =(15, 1)), sg.InputText()],
            [sg.Text('Type of Collision', size =(15, 1)), sg.InputText()],
            [sg.Text('Damages:', size =(15, 1)), sg.InputText()],
            [sg.Text('Casualty:', size =(15, 1)), sg.InputText()],
            [sg.Text('Insurance ID 1:', size =(15, 1)), sg.InputText(),
            sg.Text('Insurance ID 2:', size =(15, 1)), sg.InputText()],
            [sg.Text('Street:', size =(15, 1)), sg.InputText()],
            [sg.Text('State:', size =(15, 1)), sg.InputText()],
            [sg.Text('Date', size =(15, 1)), sg.InputText()],
            [sg.Submit('Insert')],
            [sg.Button('Exit')]
        ]
        window = sg.Window("Report Accident", layout, margins=(100,200),modal=True)
        choice = None
        
        while True:
            event, values = window.read()
            c = _conn.cursor()

            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "Insert":
                temp = [0] * 12
                
                temp[0] = values[1]
                temp[1] = values[2]
                temp[2] = "C11"
                temp[3] = values[3]
                temp[4] = values[4]
                temp[5] = values[5]
                temp[6] = values[6]
                temp[7] = values[7]
                temp[8] = values[8]
                temp[9] = values[9]
                temp[10] = "3"
                temp[11] = values[10]
            
                c.execute(
                """INSERT INTO Collision(n_name1, n_name2, n_collisionkey, n_collisiontype, n_damages,n_casualty,
                n_insurancekey1, n_insurancekey2,  n_location,n_statekey,
                n_companykey,n_date) 
                VALUES(?,?,?, ? , ?, ?, ?, ?,?,?,?,?)""" ,  
                (
                temp[0] ,
                temp[1] ,
                temp[2] ,
                temp[3] ,
                temp[4] ,
                temp[5] ,
                temp[6] ,
                temp[7] ,
                temp[8] ,
                temp[9] ,
                temp[10],
                temp[11],
                )
            )

                _conn.commit()
            
        window.close()
       
def open_Spec(_conn, dbFile):

    layout = [
        [sg.Image("glass.PNG")],
        [sg.Button("General Search", key="general"),
        sg.pin(sg.Button("Targeted Search", key="advanced"))],
        [sg.Button('Exit')]
        ]

    
    window = sg.Window("Search", layout, margins=(130,300),modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "general":
                open_General(_conn, dbFile)    
        if event == "advanced":
                open_Advanced(_conn, dbFile)  
   
    window.close()
    
def open_General(_conn, _dbFile):
    layout = [
        [sg.Image("glass.PNG")],
        [sg.Text("Select Search Type: ")],
        [sg.Button('Search by Name', key = "name")],
        [sg.Button('Search by Collision Type', key = "Type")],
        [sg.Button('Search by Date', key = "date")],
        [sg.Button('Exit')]
    ]
    window = sg.Window("Second Window", layout, margins=(130,300),modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "name":
            byName(_conn, _dbFile)
        if event == "type":
            byType(_conn, _dbFile)  

        if event == "date":
            byKey(_conn, _dbFile)    
    window.close()

def byName(_conn, _dbFile):
        layout = [
            [sg.Text('Enter Name', size =(15, 1)), sg.InputText()],
            [sg.Submit('Insert')],
            [sg.Button('Exit')]
        ]
        window = sg.Window("Search By Name", layout, margins=(130,300),modal=True)
        choice = None
        
        while True:
            event, values = window.read()
            c = _conn.cursor()

            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "Insert":
                temp = values[0]
                c.execute(f"""
                SELECT *
                FROM COLLISION
                WHERE n_name1 = '{temp}' 
                OR    n_name2 = '{temp}'
                """)
                result = c.fetchall()
                order = "Name 1	| Name 2 | collision type | damages | casualty | insurancekey 1 | insurancekey 2 | location| State | Collision key | Date | Company key"
                open_DISPLAY(_conn,_dbFile,order , result)
 

              
        window.close()

def byType(_conn, _dbFile):
        layout = [
            [sg.Text('Enter Type', size =(15, 1)), sg.InputText()],
            [sg.Submit('Insert')],
            [sg.Button('Exit')]
        ]
        window = sg.Window("Search By Type", layout, margins=(130,300),modal=True)
        choice = None
        
        while True:
            event, values = window.read()
            c = _conn.cursor()

            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "Insert":
                temp = values[0]
                c.execute(f"""
                SELECT *
                FROM COLLISION
                WHERE n_collisiontype = '{temp}'
                """)
                result = c.fetchall()
                open_DISPLAY(_conn,_dbFile,result)
    
        window.close()

def byKey(_conn, _dbFile):
        layout = [
            [sg.Text('Enter Key', size =(15, 1)), sg.InputText()],
            [sg.Submit('Insert')],
            [sg.Button('Exit')]
        ]
        window = sg.Window("Search By Key", layout, margins=(130,300),modal=True)
        choice = None
        
        while True:
            event, values = window.read()
            c = _conn.cursor()

            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "Insert":
                temp = values[0]
                c.execute(f"""
                SELECT *
                FROM COLLISION
                WHERE n_collisionkey = '{temp}'
                """)
                result = c.fetchall()
                order = "Name 1	| Name 2 | collision type | damages | casualty | insurancekey 1 | insurancekey 2 | location| State | Collision key | Date | Company key"
                open_DISPLAY(_conn,_dbFile,order , result)
 
        window.close()
        
def open_Advanced(_conn, _dbFile):
        
        layout = [
            [sg.Image("glass.PNG")],
            [sg.Text('Enter Key', size =(15, 1)), sg.InputText()],
            [sg.Submit('Insert')],
            [sg.Button('Exit')]
        ]
        window = sg.Window("Search By Key", layout, margins=(130,300),modal=True)
        choice = None
        
        while True:
            event, values = window.read()
            c = _conn.cursor()

            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "Insert":
                temp = values[1]
                c.execute(f"""
                SELECT *
                FROM COLLISION
                WHERE n_collisionkey = '{temp}'
                """)
                result = c.fetchall()
                order = "Name 1	| Name 2 | collision type | damages | casualty | insurancekey 1 | insurancekey 2 | location| State | Collision key | Date | Company key"
                open_DISPLAY(_conn,_dbFile,order , result)
 
        
        window.close()

def byType(_conn, _dbFile):
        layout = [
            [sg.Text('Enter Type', size =(15, 1)), sg.InputText()],
            [sg.Submit('Insert')],
            [sg.Button('Exit')]
        ]
        window = sg.Window("Search By Type", layout, margins=(130,300),modal=True)
        choice = None
        
        while True:
            event, values = window.read()
            c = _conn.cursor()

            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "Insert":
                temp = values[0]
                c.execute(f"""
                SELECT *
                FROM COLLISION
                WHERE n_collisiontype = '{temp}'
                """)
                result = c.fetchall()
                order = "Name 1	| Name 2 | collision type | damages | casualty | insurancekey 1 | insurancekey 2 | location| State | Collision key | Date | Company key"
                open_DISPLAY(_conn,_dbFile,order , result)
 
def byDate(_conn, _dbFile):
        layout = [
            [sg.Text('Enter Date in xxxx-xx-xx Formant', size =(15, 1)), sg.InputText()],
            [sg.Submit('Insert')],
            [sg.Button('Exit')]
        ]
        window = sg.Window("Search By Date", layout, margins=(130,300),modal=True)
        choice = None
        
        while True:
            event, values = window.read()
            c = _conn.cursor()

            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "Insert":
                temp = values[0]
                c.execute(f"""
                SELECT *
                FROM COLLISION
                WHERE n_date LIKE= '%{temp}%'
                """)
                result = c.fetchall()
                order = "Name 1	| Name 2 | collision type | damages | casualty | insurancekey 1 | insurancekey 2 | location| State | Collision key | Date | Company key"
                open_DISPLAY(_conn,_dbFile,order , result)
        
def open_DISPLAY(_conn, _dbFile,order, temp):
    layout = [
    
    [sg.Text("RETRIEVED DATA::")],
    [sg.Text("____________________")],
    [sg.Text(order)],
    [sg.Text("____________________")],
    [sg.Text(temp)],
    [sg.Button('Exit')]
    ]
    window = sg.Window("DATA", layout, margins=(130,300),modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()

def open_DISPLAY2(_conn, _dbFile, temp):
    layout = [
    
    [sg.Text("RETRIEVED DATA::")],
    [sg.Text("____________________")],
    [sg.Text(temp[0])],
    [sg.Button('Exit')]
    ]
    window = sg.Window("DATA", layout, margins=(130,300),modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()

def open_Tips(_conn, _dbFile):
    layout = [
        [sg.Image("wrench.PNG")],
        [sg.Text("UNDER CONSTRUCTION")],
        [sg.Button('Exit')]]
    window = sg.Window("Tips", layout, margins=(130,300),modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
    window.close()

def open_insurance(_conn, _dbFile):
    layout = [
        [sg.Image("wrench.PNG")],
        [sg.Text("UNDER CONSTRUCTION")],
        [sg.Button('Exit')]]
    window = sg.Window("Insurance", layout, margins=(130,300),modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()

def open_Test(_conn, _dbFile,temp):
    layout = [[sg.Text(temp)],
            [sg.Button('Confirm', key = '_CONFIRM_', visible=True),
            sg.pin(sg.Button('1', key = '_1_', visible=True)),
            sg.pin(sg.Button('2', key = '_2_', visible=True)),]
    ]
    window = sg.Window("Second Window", layout, margins=(130,300),modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
    window.close()

def main():
    database = r"traffic.sqlite"

    # create a database connection
    conn = openConnection(database)

    runGUI(conn, database)

    closeConnection(conn, database)

if __name__ == '__main__':
    main()