# 530-p2p
A peer to peer communication system for EC530 Hackathon 1.

## Authors: Kira Milgram and Daniel Paganelli

This peer-to-peer (p2p) client utilizes UDP packet protocols with unique headers to create a flexible
messaging system that allows you to speak to multiple friends at once!

## Use

## Design

### Main functionality

The p2p client is split into two simultaneous threads: send() and recv(). These function simultaneously
as a user and a client, allowing for constant, asychronous communication. When the program is first booted,
it checks if there is an existing database, and creates one if it does not find one. Then, it starts
both the send and recv threads, and finally it calls send_ping() to alert all known other users that
the current user is now online. At this point, the user may begin sending chat messages, defaulting to
messaging the most recent chat partner.

All p2p chat clients listen on the same port, simplifying socket binding and discovery. To deliniate who is 
sending what message, each packet has a robust header than includes the name of the sender and their MAC address,
which functions as a unique ID.

Each user has a unique database that stores all messages sent to and received from others. These databases do not 
interact with other users databases, relying on the individual p2p-clients to maintain their own integreity. The database
is elaborated on below, but broadly functions to save known contacts for each of communication, save conversations for later 
examination, and to reserve unsent messages in case a user is offline.

Functions:

```
send()

send is a permanently running thread that waits for user input and sends them as headered UDP packets to the desired
recipient. To provide additional functionality, when certain input is entered send() performs new tasks:

change(): Change messaging target. The client asks if the new target is a new contact (answered by entering new()) or
an already known one (answered by entering known()). If it is a new contact, the user is prompted to enter the name and
IP address of the user. If it is an already known contact, the user is prompted for a name which is used to search the database.
The client then continues functioning as normal.

ping(): The client executes send_ping() as if the program has just started running. This is a broadcast to ALL known contacts.

quit()): The client gracefully exits both the send() and recv() threads and relenquishes socket bindings.
```

```
recv()

recv() is a permanently running thread that listens constantly for incoming packets. When a packet is received, the
function checks the type of the packet, and behaves accordingly:

Type == message: The client prints the name of the sender and the message contents. It takes the message ID of the packet
and sends it as the contents of an ACK packet to the sender. The message is saved to the database with an ACK status of 0 (unACK'd).

Type == ACK: The client updates the status of the message whose ID is in the message contents to be acknowledged.

Type == ping: The client runs get_all_unsent(sender) to retrieve all messages that the client has previously sent to the
querying sender and sends them one by one.
```

```
send_ping(my_MAC)

send_ping() queries the database for all known users that are not the current user. It then takes this
information and fills out a udp packet for each known user that is specifically typed as a ping. It returns 0.
The function does not listen for replies, and instead relies on the recv thread function to be running for replies.
By default, send_ping is ran once when a user comes online, but can be called manually by typing "ping()" while
in the chat client. The response to a ping request is detailed in recv.
```



### UDP Packet Design

By its nature UDP is a low information and unreliable messaging system. The p2p-client system accounts for that by
designing unique headers built into a UDP_packet class. The structure of a UDP_packet object has the following fields:

```
- id: The ID of the message in the sender's database. Used by ACK packages to inform a client that its messages have been
received successfully.
- type: Can be "message", "ACK", or "ping". Determines what the packet is and how clients should behave on receiving the packet.
- recipient: The name of the recipient.
- sender: The name of the sender.
- message: The message contents. When the message is an ACK, the contents are always the id of the ACK'd message.
- ack_status: can be 0 (unACK'd) or 1 (ACK'd). This information is stored so that the database only sends unACK'd packets upon a ping
request.
```

### Database

The database is formed from two tables, user and messages. User saves information about the client and all known contacts, and messages
saves all messages that pass through the client, to or from.

```
user:
- name: The name of the contact. Chosen by the user when they make a new contact.
- last_ip: The last known IP of the contact. Chosen by the user when they create a new contact.
- MAC: The MAC address of the user. Filled out when a message is recieved.
- active: 0 (unactive) or 1 (active). Informs the client whether to print a warning that a contact isn't available.
```

```
messages:
- Primary Key (Integer, Autoincrement, not Null): The unique (To the specific databases involved) id of a message.
Used to keep track of ACKs.
- type (Text): The type of the message, "message", "ACK", or "ping".
- recipient (Text): The name of the recipient.
- sender (Text): The name of the sender.
- message (Text): The body of the packet. When the packet is an ACK, the message of the text is the ID of the ACK'd packet. ACKs are 
not saved in the database.
- ack_Status (Int): 0 (unACK'd) or 1 (ACK'd). Track the status of a packet, which is used to inform the client if the message should be dumped
to a contact on a ping request.

