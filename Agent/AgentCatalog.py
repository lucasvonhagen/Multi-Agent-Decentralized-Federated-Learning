
import socket, socketserver, threading
import CatalogConnectionHandler
import TCPServerCustom


#Class creating updated list of active agents available for query and listening for connections
class AgentCatalog(threading.Thread):
    
    # returns list of registered agents, syncronized
    def getList(self):
        self.eventGet.wait() # wait for other threads...
        self.eventGet.clear() # lock from other threads
        retVal=self.__getList() # access list
        self.eventGet.set() # open for other threads
        return retVal
    
    def __getList(self):
        return self.list.copy()
    
    # updates list of registered agent, syncronized
    def updateList(self, adress):
        #print("update list called in catalog with arg: ", adress)
        self.eventUpdate.wait()
        self.eventUpdate.clear()
        self.__updateList(adress)
        self.eventUpdate.set()
        print("current list: ", self.list)

    def __updateList(self, adress):
        self.list.append(adress)
        
    def run(self):
        print("catalog running")
        with TCPServerCustom.TCPServerCustom((self.ip, self.port), CatalogConnectionHandler.CatalogConnectionHandler, self) as sock:
            sock.serve_forever()

    def __init__(self, ip, port):
        self.ip=ip
        self.port=port
        self.list=list()
        self.eventGet=threading.Event()
        self.eventUpdate=threading.Event()
        self.eventGet.set() #flags true on start-up: functions available for calls by threads
        self.eventUpdate.set()
        threading.Thread.__init__(self)
        self.start()
    
    def getIp(self):
        return self.ip
    
    def getPort(self):
        return self.port

