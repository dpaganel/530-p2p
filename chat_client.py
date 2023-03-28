import socket
import threading
import os

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 9000))

name = input("your username: ")
print("--- Chat Opened ---")

def send():
    while True:
        message = input()

        if message == "quit()":
            # end the chat
            os.exit(1)
        sm = "{}  : {}".format(name, message)
        s.sendto(sm.encode(), ("127.0.0.1",9000))

def rec():
    while True:
        message = s.recv(1024)
        print("\t\t\t\t" + message[0].decode())

# create two threads, one to send messages and one to receive
t1 = threading.Thread(target=send)
t2 = threading.Thread(target=rec)

t1.start()
t2.start()