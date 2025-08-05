
import socket, socketserver, threading, _thread
from MessageTypes import MessageTypes
from Message import Message
import ConnectionHandler
import TCPServerCustom
import Agent
import pickle
import queue


#Listener for incomming connections, message-handling, message-queue?, list of discovered agent-adresses. 
class Communication(threading.Thread):

    def run(self):
        with TCPServerCustom.TCPServerCustom((self.ip, self.port_comm), ConnectionHandler.ConnectionHandler, self) as sock:
            sock.serve_forever()

    def handleMessages(self):
        while True:
            while not self.messageBuffer.empty():
                #print("buffer !empty")
                message=self.messageBuffer.get()
                messageType=message.getType()
                messageDescription=message.getDescription()
                match messageType:

                    case MessageTypes.INFORM: #information from other agent or from catalog
                        #print("inform")
                        match messageDescription:
                            case "CatalogResponse":
                                #print("cata response")
                                if(message.getContent()=="ack"):
                                    #print("ack!")
                                    self.controller.register()
                                else:
                                    self.controller.discover(message.getContent())
                            
                            #**********case federation form here!!!********
                            case "Aggregator": #behövs kanske check för "krock"?
                                self.controller.setAggregator(message.getSender())
                                message=Message((self.ip, self.port_comm),
                                                message.getSender(),
                                                MessageTypes.INFORM,
                                                "AggregatorResponse",
                                                "ack")
                                self.sendMessage(message)

                            case "AggregatorResponse":
                                if(message.getContent()=="ack"):
                                    self.controller.addFederationMember(message.getSender())

                            case "Reward":
                                print(self.clientId ," received reward: ", message.getContent())
                                message=Message((self.ip, self.port_comm),
                                                message.getSender(),
                                                MessageTypes.INFORM,
                                                "RewardResponse",
                                                "ack")
                                self.sendMessage(message)
                                
                            case "Weight":
                                print(self.clientId ," :received weights")
                                self.controller.collectWeights(message.getContent())

                            case "AggregatedWeights":
                                print(self.clientId ," received aggregated weights")
                                self.controller.collectWeights(message.getContent())
                                self.controller.register()

                            


                    case MessageTypes.REQUEST: #another agent request action
                        pass

                    case MessageTypes.AGREE: # another agent agrees to carry out requested action
                        pass

                    case MessageTypes.CFP: #another agent requests proposals
                        print(self.clientId, " :received CFP")
                        self.controller.beginNegotiation(message.getSender())

                    case MessageTypes.ACCEPT: #another agent accepted proposal
                        self.controller.addCommitment(message.getContent())
                        
                        #*********broadcast for federation formation here!********
                    
                    case MessageTypes.REJECT: #another agent rejected proposal
                        pass #either new proposal incomming or final rejection

                    case MessageTypes.PROPOSE: #another agent presents a proposal
                        self.controller.addCommitmentForEvaluation(message.getContent())
                
                    

    def addMessage(self, message):
        self.messageBuffer.put(message)

    def sendMessage(self, message):
        data=pickle.dumps(message)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((message.getReceiver()[0], message.getReceiver()[1]))
            sock.sendall(data)
            sock.close()


    def __init__(self, ip, port_comm, controller):
        self.ip=ip
        self.port_comm=port_comm
        self.clientId = port_comm
        self.controller:Agent.Agent=controller
        self.messageBuffer=queue.Queue()
        messageHandler=threading.Thread(target=self.handleMessages)
        messageHandler.start()

        print("init comms at: ", self.ip, ";", self.port_comm)
        threading.Thread.__init__(self)
        self.start()

    def getIp(self):
        return self.ip
    
    def getPort(self):
        return self.port_comm
        

    
    