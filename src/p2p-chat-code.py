import os
import socket
import pickle
import threading 
import sys
from p2pdb import *
import uuid
import components.UDP_packet as packet

# udp_packet = packet.UDP_packet("beans", "recipient", "sender", "recv_ip", "send_ip", "recv_MAC", "send_MAC", "message", "ack_status")
# print(udp_packet)


# send_ip = input("Your system's IP address: ")
# send_port = int(input("Your system's port: "))
# recv_ip = input("recv ip: ")
# recv_port = int(input("recv port: "))

# hard coded right now, could get input from user or system though! ^^
my_ip = '192.168.56.1'
my_port = 4444
receiver_ip = '192.168.56.1'
receiver_port = 4444

# bind port to socket on current platform
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((my_ip, my_port))

# when this program runs, add a user to the database
user_name = input("Enter your user name: ")
my_MAC = hex(uuid.getnode())

# make sure to set the active status to 1 because the user is on!
create_user(user_name, my_ip, my_MAC, 1)

# now we want to see who else is available


# define send functionality, encode message and send to receiving ip/port
def send():
    while True:
        message_text = input("")

        # create a message object to be put in the database
        # udp_packet = packet.UDP_packet("beans", "recipient", "sender", "recv_ip", "send_ip", "recv_MAC", "send_MAC", "message", "ack_status")
# print(udp_packet)
        udp_packet = packet.UDP_packet("message", "recipient", "user_name", receiver_ip, my_ip, "recv_MAC", my_MAC, message_text, 0)
        message_id = save_msg(udp_packet)
        udp_packet.setId(message_id)

        # quit if the message is quit()
        if (message_text == "q" or message_text == "quit"):
            print("did you mean to use quit()?")
        if message_text == "quit()":

            quit_message = "Other person has left the chat"
            udp_packet.setMessage(quit_message)
            s.sendto(pickle.dumps(udp_packet), (receiver_ip, receiver_port))
            update_user(hex(uuid.getnode()), 0, 'active')
            os._exit(1)

        s.sendto(pickle.dumps(udp_packet), (receiver_ip, receiver_port))

# define receiving functionality, decode message and print to screen
def recv():
    while True:
        udp_packet = pickle.loads(s.recv(1024))

        # go to the database and change the ack on the message to 1
        print("message received: " + udp_packet.getMessage())
        update_status(udp_packet.getId())

# utilize threads to enable sending and receiving concurrently.
t1 = threading.Thread(target=send)
t2 = threading.Thread(target=recv)
t1.start()
t2.start()