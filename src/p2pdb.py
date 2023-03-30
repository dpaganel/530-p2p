# Database module utilizing sqlite3 for the peer to peer client
# Project
import sqlite3
import os
import yaml
import time


# Initialize the database, if it hasn't been created already
def createDB():
    db, code = get_config()
    if code < 0:
        return -3
    
    con = sqlite3.connect(db)

    cur = con.cursor()

    cur.execute("CREATE TABLE user(name, last_p, MAC)")
    cur.execute("CREATE TABLE messages(sender, receiver, text, timestamp)")
    cur.execute("CREATE TABLE buffer(receiver, target_ip, text, timestamp)")

    cur.close()
    con.close()
    return 0

def get_config():
    # set path to local file
    try:
        with open(os.path.abspath("config.yaml"), 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            db = config["database"]
            f.close()
            return db, 0
    except Exception as e:
        print(e)
        print("CRITICAL ERROR: The config file does not exist!")
        return -1, -3

    finally:
        return -1, -4
    
# Save a recieved message along with a timestamp, the user who made it,
# and a session id (?)
def saveRcvMsg(msg):
    db, code = get_config()
    if code < 0:
        return -3 # config does not exist
    
    try:
        if(os.path.exists(os.path.abspath(db)) == False):
            print(db, " does not exist.")
            return -1
    except Exception as e:
        print(e)
        return -1 #db does not exist

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -2 # fail to connect to db
    
    # TODO: Finish

    return 0

# Save a message we made to the database
def saveSentMsg():
    db, code = get_config()
    if code < 0:
        return -3 # config does not exist
    
    try:
        if(os.path.exists(os.path.abspath(db)) == False):
            print(db, " does not exist.")
            return -1
    except Exception as e:
        print(e)
        return -1 #db does not exist

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -2 # fail to connect to db
    
    # TODO: Finish
    
    return 0

# Print out all of the messages in a session
def printSession():

    return 0

# Print out all of the messages to and from a user
def printUserMsgs():

    return 0

# Save a message that could not be sent due to closed or faulty connection
def storeMsg(msg):
    db, code = get_config()
    if code < 0:
        return -3 # config does not exist
    
    try:
        if(os.path.exists(os.path.abspath(db)) == False):
            print(db, " does not exist.")
            return -1
    except Exception as e:
        print(e)
        return -1 #db does not exist

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -2 # fail to connect to db

    msg_comps = msg.split("|")
    data = (msg_comps[1], msg_comps[2], msg_comps[6], msg_comps[5])

    try:
        cur.execute("INSERT INTO user VALUES(?, ?, ?,)", (data,))
        con.commit()
    except:
        cur.close()
        con.close()
        return -4 # failure to insert

    return 0

# Get all messages stored for a particular user and delete them from the database
# Used for when messages are written to an unresponding host.
def flushStoredMsgs(recipient, target_ip):
    db, code = get_config()
    if code < 0:
        return -3 # config does not exist
    
    try:
        if(os.path.exists(os.path.abspath(db)) == False):
            print(db, " does not exist.")
            return -1
    except Exception as e:
        print(e)
        return -1 #db does not exist
    
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -2 # fail to connect to db

    query = (recipient, target_ip)
    res = cur.execute("SELECT * FROM buffer WHERE receiver=(?) AND target_ip=(?)", (query,))

    res = res.fetchall()
    cur.close()
    con.close()

    msgs = res
    return msgs, 0


### TESTING FUNCTIONS ###

# Delete an existing database to create a clean slate. Use only
# for testing.
def killAndCreateDB():
    code, db = get_config()
    if code < 0:
        return code, -1
        
    if(os.path.exists(os.path.abspath(db)) == True):
        os.remove(db)
    con = sqlite3.connect(db)

    cur = con.cursor()

    cur.execute("CREATE TABLE user(name, last_p, MAC)")
    cur.execute("CREATE TABLE messages(sender, receiver, text, timestamp)")
    cur.execute("CREATE TABLE buffer(receiver, target_ip, text, timestamp)")

    cur.close()
    con.close()
    return 0




