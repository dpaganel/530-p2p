import os
import socket
import threading 
import sys
from p2pdb import *
import uuid

# send_ip = input("Your system's IP address: ")
# send_port = int(input("Your system's port: "))
# recv_ip = input("recv ip: ")
# recv_port = int(input("recv port: "))

# hard coded right now, could get input from user or system though! ^^
receiver_ip = '192.168.56.1'
receiver_port = 4444
my_ip = '192.168.56.1'
my_port = 2222

# bind port to socket on current platform
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((my_ip, my_port))

# when this program runs, add a user to the database
user_name = input("Enter your user name: ")

# make sure to set the active status to 1 because the user is on!
t3 = threading.Thread(target=create_user, args=(user_name, my_ip, hex(uuid.getnode()), 1))
t3.start()

# define send functionality, encode message and send to receiving ip/port
def send():
    while True:

        # format of a message package
        # Type|Recipient Name|Sender Name|Recipient IP|Sender IP|Recipient MAC|Sender MAC|Message I|Timestamp|Message Text

        message = input("")

        # quit if the message is quit()
        if message == "quit()":

            quit_message = "Other person has left the chat"
            s.sendto(quit_message.encode(), (receiver_ip, receiver_port))
            os._exit(1)

        s.sendto(message.encode(), (receiver_ip, receiver_port))
        print(s)

# define receiving functionality, decode message and print to screen
def recv():
    while True:
        message_recv = s.recvfrom(1024)
        print("message received: " + message_recv[0].decode())

# utilize threads to enable sending and receiving concurrently.
t1 = threading.Thread(target=send)
t2 = threading.Thread(target=recv)
t1.start()
t2.start()