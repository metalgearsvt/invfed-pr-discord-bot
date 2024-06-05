import sqlite3

# TABLE NAMES
TABLE_CONFIG = "config"
TABLE_NICK_HISTORY = "username_history"

# NICK HISTORY COLUMNS
HISTORY_PKID = "PKID"
HISTORY_USER_ID = "user_id"
HISTORY_USERNAME = "username"
HISTORY_TIMESTAMP = "timestamp"

# CONFIG ROWS
CONFIG_NICK_CHANNEL = "nick_channel"

# LIMITS
LIMIT_HISTORY = 10

####################
# NICKNAME MGMT
####################

def addNameHistory(conn: sqlite3.Connection, id, nick):
    """
    Adds a username to the history for that user.

    Parameters
    ----------
    conn : sqlite3.Connection
        The DB connection.
    id : String
        The user ID.
    nick : String
        The nickname for that user.
    """
    sql = f'''
        INSERT INTO {TABLE_NICK_HISTORY}(user_id, username)
        VALUES (?,?)
        '''
    vals = (id, nick)
    cur = conn.cursor()
    cur.execute(sql, vals)
    conn.commit()
    cur.close()

def fetchLimitedNameHistory(conn: sqlite3.Connection, id):
    """
    Fetches the last datalayer.LIMIT_HISTORY usernames for id.

    Parameters
    ----------
    conn : sqlite3.Connection
        The DB connection.
    id : String
        The user ID to fetch usernames for.
    
    Return
    ------
    usernames : List
        A list of the usernames.
    """
    sql = f'''
        SELECT username FROM {TABLE_NICK_HISTORY}
        WHERE {HISTORY_USER_ID} = ?
        ORDER BY {HISTORY_TIMESTAMP} DESC
        LIMIT {LIMIT_HISTORY}
    '''
    vars = (id,)
    cur = conn.cursor()
    cur.execute(sql, vars)
    usernames = cur.fetchall()
    return usernames

####################
# CONFIG VALUES
####################

def updateNickChannel(conn: sqlite3.Connection, channel):
    """
    Updates the NickChannel config.

    Parameters
    ----------
    conn : sqlite3.Connection
        The DB connection.
    channel : String
        The channel ID.
    """
    sql = f'''
        INSERT OR REPLACE INTO {TABLE_CONFIG}(key, value)
        VALUES (?,?)
        '''
    vals = (CONFIG_NICK_CHANNEL, channel)
    cur = conn.cursor()
    cur.execute(sql, vals)
    conn.commit()
    cur.close()

def fetchConfigValue(conn: sqlite3.Connection, key):
    """
    Returns the a config value for the given key.

    Parameters
    ----------
    conn : sqlite3.Connection
        The DB connection.
    key : String
        The config key to fetch the value of.
    
    Returns
    -------
    value : String
        The configured value for the given key, or None if not set.
    """
    sql = f'''SELECT value FROM {TABLE_CONFIG} WHERE key = ?'''
    vals = (key,)
    cursor = conn.cursor()
    try:
        cursor.execute(sql, vals)
        configVal = cursor.fetchone()[0]
        return configVal
    except Exception as e:
        print(e)
        return None

####################
# DB MAINTENANCE
####################

def checkDb(conn: sqlite3.Connection):
    """
    Checks to see if the database needs to be initialized, and does it if so.
    It does this by checking to see if the config table exists.

    Parameters
    ----------
    conn : sqlite3.Connection
        The DB connection.
    """
    sql = f'''SELECT * FROM {TABLE_CONFIG}'''
    cur = conn.cursor()
    try:
        # We are going to try to run this command.
        # If the table doesn't exist we will get an OperationalError.
        rows = cur.execute(sql)
    except sqlite3.OperationalError:
        initialize(conn)

def initialize(conn: sqlite3.Connection):
    """
    Initializes the database by creating tables, handling gracefully if rows/tables already exist.
    
    Parameters
    ----------
    conn : sqlite3.Connection
        The DB connection.
    """
    print("Need to init!")
    cursor = conn.cursor()
    # Create the configuration table.
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_CONFIG} (
                   "key"        TEXT,
                   "value"      TEXT,
                   PRIMARY KEY("key")
        )''')
    print(f"Created {TABLE_CONFIG} table.")
    # Create the table to hold the username history.
    # The column PKID being INTEGER PRIMARY KEY will auto increment if not supplied a value.
    # The reason we're using this as a PK is because the same user could
    # have the same name multiple times, and creating a 3 column PK is a pain.
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NICK_HISTORY} (
                   "PKID"       INTEGER PRIMARY KEY,
                   "user_id"    TEXT,
                   "username"   TEXT,
                   "timestamp"  DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    print(f"Created {TABLE_NICK_HISTORY} table.")
    conn.commit()
    print("Committed changes.")
