# create a class to make message packets uniform
            # format of a message package
            # Type|Recipient Name|Sender Name|Recipient IP|Sender IP|Recipient MAC|Sender MAC|Message I|Timestamp|Message Text
class UDP_packet:
    def __init__(self, type, recipient, sender, message, ack_status):
        self.id = 0
        self.type = type
        self.recipient = recipient
        self.sender = sender
        self.message = message
        self.ack_status = ack_status
    
    def setId(self, id):
        self.id = id
    def getId(self):
        return self.id
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
    def setMessage(self, message):
        self.message = message
    def getMessage(self):
        return (self.message)
    def setAck_status(self, ack_status):
        self.ack_status = ack_status
    def getAck_status(self):
        return (self.ack_status)