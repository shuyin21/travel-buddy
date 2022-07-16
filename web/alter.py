import sqlite3 as sql


def databaseCon():
    conn = sql.connect("web/travel-db.db")
    
    conn.row_factory = sql.Row
    return conn


conn = databaseCon()
mycursor = conn.cursor()
mycursor.execute("ALTER TABLE members ADD saved_traveler varchar(255);")