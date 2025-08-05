#help-class handling incomming connections to Communication-class
import socket, socketserver
import pickle

class ConnectionHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data =b""
        while True:
            inc=self.request.recv(1024)
            if not inc:
                break
            self.data+=inc
        data_deserialized=pickle.loads(self.data)
        self.controller=self.server.controller
        self.controller.addMessage(data_deserialized)
        
        