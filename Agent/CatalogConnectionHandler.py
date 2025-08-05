import socket, socketserver
from Message import Message
from MessageTypes import MessageTypes
import AgentCatalog
import pickle


class CatalogConnectionHandler(socketserver.BaseRequestHandler):
    
    def sendMessage(self, message):
        data=pickle.dumps(message)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((message.getReceiver()[0], message.getReceiver()[1]))
            sock.sendall(data)
            sock.close()

    def handle(self):
        self.data = self.request.recv(1024)
        message=pickle.loads(self.data)
        self.controller=self.server.controller
        self.controllerIp=self.controller.getIp()
        self.controllerPort=self.controller.getPort()

        messageType=message.getType()
        messageDescription=message.getDescription()
        if(messageType==MessageTypes.REQUEST):
            if(messageDescription=="register"):
                print("catalog accepted connection from: ", message.getSender()[0], ";", message.getSender()[1])
                self.controller.updateList(message.getSender())
                messageReply=Message((self.controllerPort, self.controllerIp),
                                     (message.getSender()[0], message.getSender()[1]),
                                     MessageTypes.INFORM,
                                     "CatalogResponse",
                                     "ack")
                self.sendMessage(messageReply)
            elif(messageDescription=="list"):
                self.list=self.controller.getList()
                print("catalog sending list to: ", message.getSender()[0], ";", message.getSender()[1])
                messageReply=Message((self.controllerPort, self.controllerIp),
                                     (message.getSender()[0], message.getSender()[1]),
                                     MessageTypes.INFORM,
                                     "CatalogResponse",
                                     self.list)
                self.sendMessage(messageReply)

        
    