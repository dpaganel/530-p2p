# Message Format

Due to the limited nature of UDP we are implementing our own packet format to be sent. This has been implemented as a UDP_package class that has the following schema:

UDP_packet:
- id
- type
- recipient id
- sender id
- message text
- ack status

where ack_status can have one of two values: 0 (sent), 1 (received)



# Database Schema


## Users
A table to store userdata and the data of other known users. MAC addresses, being unique and immutable per device, are used in place of user ids.

Columns:
- name
- last_ip
- MAC
## Messages
This table is used as a local storage for all messages in the system.

Columns:
- sender
- receiver
- text
- timestamp

## buffer
This table is used to store messages that failed to send due to a closed or lost connection.

Columns:
- receiver
- target_ip
- text
- timestamp