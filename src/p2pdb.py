# Database module utilizing sqlite3 for the peer to peer client
# Project
import sqlite3
import os
import yaml

# Get the name of the db from the config file
def getDB():
    try:
        with open(os.abspath("src/config.yaml", "r")) as f:
            config = yaml.load(f, Loader = yaml.FullLoader)
            db = config["database"]
            f.close()
            return db, 0
    except Exception as e:
        print(e)
        print("CRITICAL ERROR: The config file does not exist!")
        return -1, -3

# Initialize the database, if it hasn't been created already
def createDB():
    db, code = getDB()

    if code == -3:
        return -1

    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute("CREATE TABLE storedMsgs(name, timestamp, MAC, message)")
    cur.execute("CREATE TABLE ")

    return 0

# Save a recieved message along with a timestamp, the user who made it,
# and a session id (?)
def saveRcvMsg():

    return 0

# Save a message we made to the database
def saveSentMsg():
    
    return 0

# Print out all of the messages in a session
def printSession():

    return 0

# Print out all of the messages to and from a user
def printUserMsgs():

    return 0

# Save a message that could not be sent due to closed or faulty connection
def storeMsg():

    return 0

# Get all messages stored for a particular user and delete them from the database
# Used for when messages are written to an unresponding host.
def flushStoredMsgs():
    msgs = []
    return msgs, 0


### TESTING FUNCTIONS ###

# Delete an existing database to create a clean slate. Use only
# for testing.
def killAndCreateDB():
    
    return 0




