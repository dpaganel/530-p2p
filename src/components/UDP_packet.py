# create a class to make message packets uniform
            # format of a message package
            # Type|Recipient Name|Sender Name|Recipient IP|Sender IP|Recipient MAC|Sender MAC|Message I|Timestamp|Message Text
class UDP_packet:
    def __init__(self, type, recipient, sender, recv_ip, send_ip, recv_MAC, send_MAC, message, ack_status):
        self.type = type
        self.recipient = recipient
        self.sender = sender
        self.recv_ip = recv_ip
        self.send_ip = send_ip
        self.recv_MAC = recv_MAC
        self.send_MAC = send_MAC
        self.message = message
        self.ack_status = ack_status
    
    def setType(self, type):
        self.type = type
    def getType(self):
        return (self.type)
    def setRecipient(self, recipient):
        self.recipient = recipient
    def getRecipient(self):
        return (self.recipient)
    def setSender(self, sender):
        self.sender = sender
    def getSender(self):
        return (self.sender)
    def setRecv_ip(self, recv_ip):
        self.recv_ip = recv_ip
    def getRecv_ip(self):
        return (self.recv_ip)
    def setSend_ip(self, send_ip):
        self.recv_ip = send_ip
    def getSend_ip(self):
        return (self.send_ip)
    def setRecv_MAC(self, recv_MAC):
        self.recv_MAC = recv_MAC
    def getRecv_MAC(self):
        return (self.recv_MAC)
    def setSend_MAC(self, send_MAC):
        self.send_MAC = send_MAC
    def getSend_MAC(self):
        return (self.send_MAC)
    def setMessage(self, message):
        self.message = message
    def getMessage(self):
        return (self.message)
    def setAck_status(self, ack_status):
        self.ack_status = ack_status
    def getAck_status(self):
        return (self.ack_status)