import os
import socket
import threading 

# send_ip = input("Your system's IP address: ")
# send_port = int(input("Your system's port: "))
# recv_ip = input("recv ip: ")
# recv_port = int(input("recv port: "))

send_ip = '192.168.56.1'
send_port = 4444
recv_ip = '10.0.2.15'
recv_port = 3333

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((send_ip, send_port))

def send():
    while True:
        message = input("")
        s.sendto(message.encode(), (recv_ip, recv_port))
        print(s)

def recv():
    while True:
        message_recv = s.recvfrom(1024)
        print("message received: " + message_recv[0].decode())

t1 = threading.Thread(target=send)
t2 = threading.Thread(target=recv)
t1.start()
t2.start()