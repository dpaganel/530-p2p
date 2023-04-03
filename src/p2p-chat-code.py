import os
import socket
import threading 

# send_ip = input("Your system's IP address: ")
# send_port = int(input("Your system's port: "))
# recv_ip = input("recv ip: ")
# recv_port = int(input("recv port: "))

# hard coded right now, could get input from user or system though! ^^
my_ip = '192.168.56.1'
my_port = 4444
receiver_ip = '192.168.56.1'
receiver_port = 2345

ack = "code 1: message was sent successfully"

# bind port to socket on current platform
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((my_ip, my_port))

# define send functionality, encode message and send to receiving ip/port
def send():
    while True:
        message = input("")
        s.sendto(message.encode(), (receiver_ip, receiver_port))
        print(s)

# define receiving functionality, decode message and print to screen
def recv():
    while True:
        message_recv = s.recvfrom(1024)
        message_ack = 1
        print("message received: " + message_recv[0].decode())
        if (message_recv != "message received: code 1: message was sent successfully"):
            send_ack()

def send_ack():
    s.sendto(ack.encode(), (receiver_ip, receiver_port))

# utilize threads to enable sending and receiving concurrently.
t1 = threading.Thread(target=send)
t2 = threading.Thread(target=recv)
t1.start()
t2.start()