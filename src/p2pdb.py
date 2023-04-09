# Database module utilizing sqlite3 for the peer to peer client
# Project
import sqlite3
import os
import yaml
import time
import components.UDP_packet as packet

# constants that define message status
SENT = 0
ACKED = 0
# Expected length of a packet once split
# into component parts
MSG_BLOCKS = 10
RECIPIENT_NAME_INDEX = 1
    

# Initialize the database, if it hasn't been created already
def createDB():
    db, code = get_config()
    if code < 0:
        return -3
    
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -2 # fail to connect to db

    cur = con.cursor()

    cur.execute("CREATE TABLE user(name, last_ip, MAC, active)")
    cur.execute("CREATE TABLE messages(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, type TEXT, recipient TEXT, sender TEXT, message TEXT, ack_status INT)")

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


# create a user for storage. Also usable to remember remote users.
# returns 0 on success
def create_user(user_name, user_ip, user_MAC, active):
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

    data = (str(user_name), str(user_ip), str(user_MAC))
    cur.execute("INSERT INTO user VALUES(?, ?, ?, ?)", (user_name, user_ip, user_MAC, int(active)),)

    con.commit()

    cur.close()
    con.close()
    return 0 

# return all values of a user in the form of a list (tuple?)
# given a name. Returns the tuple and a code, 0 on a success.
# On all failures the returned "user" is -1.
def get_user_by_name(name):
    db, code = get_config()
    if code < 0:
        return -1, -3 # config does not exist
    
    try:
        if(os.path.exists(os.path.abspath(db)) == False):
            print(db, " does not exist.")
            return -1
    except Exception as e:
        print(e)
        return -1, -1 #db does not exist

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -1, -2 # fail to connect to db
    
    res = cur.execute("SELECT * FROM user WHERE name=(?)", (name))
    res = res.fetchone()
    cur.close()
    con.close()
    if res is not None:
        return res, 0
    else:
        return -1, -5

# return all values of a user in the form of a list (tuple?)
# given a MAC address. Returns the tuple and a code, 0 on a success.
# On all failures the returned "user" is -1.
def get_user_by_MAC(MAC):
    db, code = get_config()
    if code < 0:
        return -1, -3 # config does not exist
    
    try:
        if(os.path.exists(os.path.abspath(db)) == False):
            print(db, " does not exist.")
            return -1
    except Exception as e:
        print(e)
        return -1, -1 #db does not exist

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -1, -2 # fail to connect to db
    
    res = cur.execute("SELECT * FROM user WHERE MAC=(?)", (MAC))
    res = res.fetchone()
    cur.close()
    con.close()
    if res is not None:
        return res, 0
    else:
        return -1, -5

# return all known users who are not us - this is used to ping
# all known contacts in order to try and get an update on what messages
# they have.
# returns a list of users in tuple form
def get_known_users(self_MAC):
    db, code = get_config()
    if code < 0:
        return -1, -3 # config does not exist
    
    try:
        if(os.path.exists(os.path.abspath(db)) == False):
            print(db, " does not exist.")
            return -1
    except Exception as e:
        print(e)
        return -1, -1 #db does not exist

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -1, -2 # fail to connect to db
    
    res = cur.execute("SELECT * FROM user WHERE MAC!=(?)", (self_MAC,))
    res = res.fetchall()

    cur.close()
    con.close()
    
    if res is not None:
        return res, 0
    else:
        return -1, -5

# Update the specific value of a specific user given
# desired values and the MAC address of the user
def update_user(user_MAC, new_data, column):
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

    if (column == 'name'):
        cur.execute("UPDATE user SET name =(?) WHERE MAC=(?)", (new_data, user_MAC))
        con.commit()
    elif (column == 'active'):
        cur.execute("UPDATE user SET active =(?) WHERE MAC=(?)", (new_data, user_MAC))
        con.commit()
    elif (column == 'last_ip'):
        cur.execute("UPDATE user SET last_ip =(?) WHERE MAC=(?)", (new_data, user_MAC))
        con.commit()
    else:
        return -4 # improper column request

    con.commit()
    cur.close()
    con.close()

    return 0

# save a message into the conversations database.
# Functions for both inbound and outbound messages.
# Status can be either. Takes in a full message with
# custom headers and splits in function. See the README
# for message formatting.
# Return 0 on success
def save_msg(udp_packet):

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
    
    # discard msg type
    data = (None, str(udp_packet.getType()), str(udp_packet.getRecipient()), str(udp_packet.getSender()), str(udp_packet.getMessage()), str(udp_packet.getAck_status()))
    try:
        cur.execute("INSERT INTO messages VALUES(?, ?, ?, ?, ?, ?)", data)
        con.commit()
        return cur.lastrowid

    except Exception as e:
        print(e)

    cur.close()
    con.close()

    return 0

# Get all messages returned as a list of tuples(?) that have not been ack'd.
# Use it to send all messages on ping
# can specify by name of recipient or MAC address of a user as a string
def get_all_unsent(user_spec, spec_type='name'):
    db, code = get_config()
    if code < 0:
        return -1, -3 # config does not exist
    
    try:
        if(os.path.exists(os.path.abspath(db)) == False):
            print(db, " does not exist.")
            return -1
    except Exception as e:
        print(e)
        return -1, -1 #db does not exist

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -1, -2 # fail to connect to db    

    data = (user_spec, 0)

    if (spec_type == 'name'):
        res = cur.execute("SELECT * FROM conversations WHERE reciever=(?) AND ack_status=(?)", data)
        res = res.fetchall()

    elif (spec_type == 'MAC'):
        res = cur.execute("SELECT * FROM conversations WHERE to_MAC=(?) AND ack_status=(?)", data)
        users = res.fetchall()
    else:
        return -1, -4
    
    cur.close()
    con.close()

    return users, 0

# Get all messages to and from a user - a full conversation
# data_types: 'name' or 'MAC' and denotes whether the targeted
# other user should be defined by name or MAC address
# Currently does not sort conversations.
def get_full_convo(current_user, recipient, data_type='name'):
    db, code = get_config()
    if code < 0:
        return -1, -3 # config does not exist
    
    try:
        if(os.path.exists(os.path.abspath(db)) == False):
            print(db, " does not exist.")
            return -1
    except Exception as e:
        print(e)
        return -1, -1 #db does not exist

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -1, -2 # fail to connect to db
    
    if (data_type == 'name'):
        data = (recipient, recipient)
        res = cur.execute('''SELECT * FROM conversations WHERE receiver=(?) OR sender=(?)''', data)
    elif (data_type == 'MAC'):
        data = (recipient, recipient)
        res = cur.execute('''SELECT * FROM conversations WHERE to_MAC=(?) OR from_MAC=(?)''', data)
    else:
        return -1, -4 # bad data_type input
    
    res = res.fetchall()
    
    cur.close()
    con.close()

    return res, 0

# given a message id, update it from sent to ack'd
def update_status(msg_id):
    db, code = get_config()
    if code < 0:
        return -1, -3 # config does not exist
    
    try:
        if(os.path.exists(os.path.abspath(db)) == False):
            print(db, " does not exist.")
            return -1
    except Exception as e:
        print(e)
        return -1, -1 #db does not exist

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return -1, -2 # fail to connect to db
    
    data = (1, msg_id)

    cur.execute("UPDATE messages SET ack_status =(?) WHERE id=(?)", data)
    con.commit()

    cur.close()
    con.close()

    return 0


### TESTING FUNCTIONS ###

# Delete an existing database to create a clean slate. Use only
# for testing.
def killAndCreateDB():
    db, code = get_config()
    if code < 0:
        return code, -1
        
    if(os.path.exists(os.path.abspath(db)) == True):
        os.remove(db)
    createDB()

    return 0
