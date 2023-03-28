# Database module utilizing sqlite3 for the peer to peer client
# Project
import sqlite3


# Initialize the database, if it hasn't been created already
def createDB():

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




