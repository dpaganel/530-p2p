import os
import socket
import pickle
import threading 
import sys
from p2pdb import *
import uuid
import components.UDP_packet as packet

# udp_packet = packet.UDP_packet("beans", "recipient", "sender", "recv_ip", "send_ip", "recv_MAC", "send_MAC", "message", "ack_status")

# user in db: ID, Name, last_ip, MAC, active status
ID_INDEX = 0
NAME_INDEX = 1
LAST_IP_INDEX = 2
MAC_INDEX = 3
STATUS_INDEX = 4

# msg in db: ID, type, recipient, sender, msg text, ack status
MSG_RECIPIENT_INDEX = 2
MSG_SENDER_INDEX = 3
MSG_TEXT_INDEX = 4

# send_ip = input("Your system's IP address: ")
# send_port = int(input("Your system's port: "))
# recv_ip = input("recv ip: ")
# recv_port = int(input("recv port: "))

# hard coded right now, could get input from user or system though! ^^
HARDCODE_IP = True
HARDCODE_PORT = True

my_ip = ''
my_port = 4445

if HARDCODE_IP:
    receiver_ip = '128.197.29.250'
else:
    receiver_ip = input("recv ip: ")
if HARDCODE_PORT:
    receiver_port = 2223
else:
    receiver_port = int(input("recv port: "))
# bind port to socket on current platform

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((my_ip, my_port))

# when this program runs, add a user to the database
user_name = input("Enter your user name: ")
my_MAC = hex(uuid.getnode())

# make sure to set the active status to 1 because the user is on!
create_user(user_name, my_ip, my_MAC, 1)

# now we want to see who else is available
known_users = get_known_users(my_MAC)


# define send functionality, encode message and send to receiving ip/port
def send():
    while True:
        message_text = input("")

        # quit if the message is quit()
        if (message_text == "q" or message_text == "quit"):
            print("did you mean to use quit()?")
        if message_text == "quit()":

            quit_message = "Other person has left the chat"
            udp_packet.setMessage(quit_message)
            s.sendto(pickle.dumps(udp_packet), (receiver_ip, receiver_port))
            update_user(hex(uuid.getnode()), 0, 'active')
            os._exit(1)

        # create a message object to be put in the database
        # udp_packet = packet.UDP_packet("beans", "recipient", "sender", "recv_ip", "send_ip", "recv_MAC", "send_MAC", "message", "ack_status")
    # print(udp_packet)
        udp_packet = packet.UDP_packet("message", "recipient", user_name, message_text, 0)
        message_id = save_msg(udp_packet)
        udp_packet.setId(message_id)

        s.sendto(pickle.dumps(udp_packet), (receiver_ip, receiver_port))

# Send a ping message to all known users to check if they are awake
# This should be executed after the listening thread has been started as it has no way
# to get messages back itself
# pings aren't true messages and so do not get saved in the database.
def send_ping(user_list):
    udp_packet = packet.UDP_packet("ping","", user_name, "ping!", 0)
    user_list = get_known_users()
    for user in user_list:
        udp_packet.recipient = user[NAME_INDEX]
        # recv_ip = 

    return 0


# define receiving functionality, decode message and print to screen
def recv():
    while True:
        try:
            udp_packet = pickle.loads(s.recv(1024))
            if udp_packet.type == "message":
                print("message received: " + udp_packet.getMessage())
                udp_packet.ack_status = 1
                save_msg(udp_packet)

                # Send an ACK to inform the other user that their message was               
                # recieved. Note, if we get an ACK we do not need to ACK that.
                ack_packet = packet.UDP_packet("ACK", udp_packet.getSender(), user_name, udp_packet.getID(), 0)
                s.sendto(pickle.dumps(ack_packet), (receiver_ip, receiver_port))
            
            elif udp_packet.type == "ACK":
                # the message of an ACK packet is the id of the packet it is ack'ing.
                update_status(udp_packet.getMessage()) 
                # For testing:
                print("GOT an ACK! MSG ID: ", udp_packet.getMessage())

            # Packet is a ping
            else:
                sender = udp_packet.getSender()
                unsent_msgs = get_all_unsent(sender)
                for msg in unsent_msgs:
                    pkt = packet.UDP_packet("message", sender, user_name, msg[MSG_TEXT_INDEX], 0)
                    s.sendto(pickle.dumps(pkt), (receiver_ip, receiver_port))

        except Exception as e:
            # the recipient is not reachable.
            print("The message could not be delivered at this time, we will try again later.")
        # go to the database and change the ack on the message to 1


# utilize threads to enable sending and receiving concurrently.
# For testing
killAndCreateDB()

t1 = threading.Thread(target=send)
t2 = threading.Thread(target=recv)
t1.start()
t2.start()
# send_ping()