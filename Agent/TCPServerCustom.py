import socketserver
from socketserver import BaseRequestHandler


class TCPServerCustom(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, controller, bind_and_activate: bool = True) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.controller=controller