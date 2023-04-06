# Message Format

Due to the limited nature of UDP we are implementing our own headers,

They are in this format:

```
Type|Recipient Name|Sender Name|Recipient IP|Sender IP|Recipient MAC|Sender MAC|Message I|Timestamp|Message Text
```

Thus, the message can be split into its parts via the split("|") command.

This has now been changed to a UDP_package class that has the following schema:

class UDP_packet:
    def __init__(self, type, recipient, sender, recv_ip, send_ip, recv_MAC, send_MAC, message, ack_status):

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