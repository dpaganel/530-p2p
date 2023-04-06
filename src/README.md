# Message Format

Due to the limited nature of UDP we are implementing our own headers,

They are in this format:

```
Type|Recipient Name|Sender Name|Recipient IP|Sender IP|Recipient MAC|Sender MAC|Message I|Timestamp|Message Text
```

Thus, the message can be split into its parts via the split("|") command.


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