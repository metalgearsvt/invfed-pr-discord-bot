import sqlite3

def checkDb(conn):
    sql = '''SELECT value FROM config WHERE key = "usernameUpdateChannel"'''
    cur = conn.cursor()
    try:
        rows = cur.execute(sql)
        if rows.size() < 1:
            initialize(conn)
    except sqlite3.OperationalError:
        initialize(conn)

def initialize(conn):
    print("Need to init!")