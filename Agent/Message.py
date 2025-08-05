

class Message:

    def getType(self):
        return self.__type

    def getDescription(self):
        return self.__description
    
    def getContent(self):
        return self.__content
    
    def getSender(self):
        return self.__sender
    
    def getReceiver(self):
        return self.__receiver
    
    def __init__ (self, sender, receiver, type, description, content):
        self.__sender=sender
        self.__receiver=receiver
        self.__type=type
        self.__description=description
        self.__content=content
