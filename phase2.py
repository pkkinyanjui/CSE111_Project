import sqlite3
from sqlite3 import Error



def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn


def createTable(_conn):
    
    print("++++++++++++++++++++++++++++++++++")
    print("Create table")
    c = _conn.cursor()

    
    _conn.execute("BEGIN")

    try:
        sql = """create table Car (
                    c_vin decimal(11,0) not null,
                    c_model char(20) not null,
                    c_plate decimal(7) not null,
                    c_ownerkey decimal(10) not null,
                    c_title decimal(1) not null
                    )"""
        _conn.execute(sql)
        sql = """create table Insurance (
                    i_damages decimal(11) not null,
                    i_name char(20) not null,
                    i_insurancekey decimal(10) not null,
                    i_collisionkey decimal(4) not null,
                    i_statekey decimal(4) not null
                    )"""
        _conn.execute(sql)
        sql = """create table State (
                    s_statekey decimal(11) not null,
                    s_name char(20) not null
                    )"""

        _conn.execute(sql)
        sql = """create table Owner (
                    o_name char(20) not null,
                    o_ownerkey char(4) not null,
                    o_state char(12) not null,
                    o_insurancekey decimal(9) not null,
                    o_plate decimal(2) not null,
                    o_casualty char(7) not null
                    )"""
        _conn.execute(sql)
        sql = """create table Towing (
                    t_name char(20) not null,
                    t_companykey decimal(3) not null,
                    t_state char(12) not null,
                    t_collisionkey decimal(4) not null
                    )"""
        _conn.execute(sql)
        sql = """create table Collision (
                    n_collisiontype char(4) not null,
                    n_casuality decimal(3) not null,
                    n_damages decimal(11) not null,
                    n_insurancekey  decimal(4) not null,
                    n_location char(50) not null,
                    n_statekey decimal(3) not null,
                    n_collisionkey char(12) not null,
                    n_date text(7) not null
                    )"""
        _conn.execute(sql)

        _conn.execute("COMMIT")

    except Error as e:
        _conn.execute("ROLLBACK")
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def dropTable(_conn):

    print("++++++++++++++++++++++++++++++++++")
    print("Drop tables")
     
    _conn.execute("BEGIN")
        
    try:
        sql = "DROP TABLE Car"
        _conn.execute(sql)

        sql = "DROP TABLE Insurance"
        _conn.execute(sql)

        sql = "DROP TABLE State"
        _conn.execute(sql)

        sql = "DROP TABLE Owner"
        _conn.execute(sql)

        sql = "DROP TABLE Towing"
        _conn.execute(sql)

        sql = "DROP TABLE Collision"
        _conn.execute(sql)
        
        _conn.execute("COMMIT")
        print("success")
    except Error as e:
        _conn.execute("ROLLBACK")
        print(e)
    
    print("++++++++++++++++++++++++++++++++++")


def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def main():
    database = r"poop.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        dropTable(conn)
        createTable(conn)
        #populateTable(conn)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
