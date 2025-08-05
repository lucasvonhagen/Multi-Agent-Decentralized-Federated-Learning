
from Commitment import Commitment 
from ProfileManager import ProfileManager 
from CommitmentManager import CommitmentManager
from Communication import Communication
from Evaluation import Evaluation
from Negotiation import Negotiation
from Training import Training 
from States import States
from Message import Message
from MessageTypes import MessageTypes
from RuleEngine import RuleEngine
from ObjectiveTypes import ObjectiveTypes
from KnowledgeBase import KnowledgeBase
from CommitmentTypes import CommitmentTypes
from random import randint
import threading
import time
import copy
import socket
import pickle


#Main agent class containing the driving FSM.
class Agent(threading.Thread):

    def register(self):
        #print("agent registered")
        self.__registered.set()

    def discover(self, list):
        self.__contacts=list
        #print("received list from catalog: ", self.__contacts)
        self.__discovered.set()

    def addCommitmentForEvaluation(self, commitment):
        self.__commitmentManager.addCommitmentForEvaluation(commitment)

    def addCommitment(self, commitment):
        self.__commitmentManager.addCommitment(commitment)

    def getCommitments(self):
        return self.__commitmentManager.getCommitments()

    def getObjective(self):
        return self.__profileManager.getObjective()

    def beginNegotiation(self, sender):
        if(self.__currentState==States.NEGOTIATION_FEDERATION):
            objective=self.__profileManager.getObjective()
            patience=self.__ruleEngine.getPatience()
            price=self.__ruleEngine.getPrice()
            commitment=self.__negotiation.beginProposal(objective, sender, patience, price)
            message=Message((self.__ip, self.__port),
                            sender,
                            MessageTypes.PROPOSE,
                            "",
                            commitment)
            self.__communication.sendMessage(message)

    def setAggregator(self, aggregator):
        if(self.__currentState==States.TRAINING):
            self.__knowledgebase.setAggregator(aggregator)

    def addFederationMember(self, member):
        self.__knowledgebase.addMember(member)

    def collectWeights(self, weights):
        self.__evaluation.collectWeights(weights)
        

    #temp?
    def getPatience(self):
        return self.__ruleEngine.getPatience()
    
    #temp?
    def getCostLimit(self):
        return self.__ruleEngine.getCostLimit()
    
    #temp?
    def getPrice(self):
        return self.__ruleEngine.getPrice()
    
    def run(self):
            while(True):
                info=self.__currentState.name
                case=self.__currentState.value
                match case:
                    case 0: #exit
                        print(self.__port," :state: ", info)
                        return
                    case 1: #Register at catalog
                        print(self.__port," :state: ", info)
                        message=Message((self.__ip, self.__port),
                                        (self.__ipCatalog, self.__portCatalog),
                                        MessageTypes.REQUEST,
                                        "register",
                                        "")
                        self.__communication.sendMessage(message)
                        self.__registered.wait()
                        self.__nextState=States.DISCOVERY
                    case 2: #Query for agent-list
                        print(self.__port," :state: ", info)
                        print(self.__port," :waiting... ")
                        self.__sleepEvent.wait(5)
                        message=Message((self.__ip, self.__port),
                                        (self.__ipCatalog, self.__portCatalog),
                                        MessageTypes.REQUEST,
                                        "list",
                                        "")
                        self.__communication.sendMessage(message)
                        self.__discovered.wait()
                        self.__nextState=States.NEGOTIATION_FEDERATION
                        self.__discovered.clear()
                    case 3: #Negotiate commits
                        print(self.__port," :state: ", info)
                        objective=self.__profileManager.getObjective()
                        if(objective==ObjectiveTypes.IMPROVED_ACCURACY):
                            for adress in self.__contacts:
                                if(not adress==(self.__ip, self.__port)):
                                    message=Message((self.__ip, self.__port),
                                                    (adress[0], adress[1]),
                                                    MessageTypes.CFP,
                                                    "",
                                                    "")
                                    self.__communication.sendMessage(message)
                                    commitment=Commitment((self.__ip, self.__port),
                                                          (self.__ip, self.__port),
                                                          CommitmentTypes.TRAIN,
                                                          0)
                                    self.__commitmentManager.addCommitment(commitment)
                        timeStart=time.time()
                        timeCurr=time.time()
                        while(timeCurr-timeStart<25):
                            commitment=self.__commitmentManager.getCommitmentForEvaluation()
                            if(not commitment==-1):
                                result=self.__negotiation.evaluateCommitment(self.__profileManager.getObjective(),
                                                                            commitment, 
                                                                            self.__ruleEngine.getPatience(),
                                                                            self.__ruleEngine.getCostLimit(),
                                                                            self.__profileManager.getPrice())
                                match result:
                                    case -1:
                                        return #no commits to evaluate, exit
                                    case False:
                                        if(not commitment.getDebtor==(self.__ip, self.__port)):
                                            returnAdress=commitment.getDebtor()
                                        elif(not commitment.getCreditor==(self.__ip, self.__port)):
                                            returnAdress=commitment.getCreditor()
                                        message=Message((self.__ip, self.__port),
                                                        returnAdress,
                                                        MessageTypes.REJECT,
                                                        "",
                                                        "")
                                        self.__communication.sendMessage(message)
                                    case True:
                                        if(not commitment.getDebtor==(self.__ip, self.__port)):
                                            returnAdress=commitment.getDebtor()
                                        elif(not commitment.getCreditor==(self.__ip, self.__port)):
                                            returnAdress=commitment.getCreditor()
                                        message=Message((self.__ip, self.__port),
                                                        returnAdress,
                                                        MessageTypes.ACCEPT,
                                                        "",
                                                        commitment)
                                        self.__communication.sendMessage(message)
                                        self.__commitmentManager.addCommitment(commitment)
                                    case _:
                                        if(not commitment.getDebtor==(self.__ip, self.__port)):
                                            returnAdress=commitment.getDebtor()
                                        elif(not commitment.getCreditor==(self.__ip, self.__port)):
                                            returnAdress=commitment.getCreditor()
                                        message=Message((self.__ip, self.__port),
                                                        returnAdress,
                                                        MessageTypes.REJECT,
                                                        "",
                                                        "")
                                        self.__communication.sendMessage(message)
                                        message=Message((self.__ip, self.__port),
                                                        returnAdress,
                                                        MessageTypes.PROPOSE,
                                                        "",
                                                        result)
                                        self.__communication.sendMessage(message)
                            timeCurr=time.time()
                        self.__nextState=States.TRAINING
                    case 4: #Training
                        print(self.__port," :state: ", info)
                        self.__nextState=States.DISCOVERY
                        commits = self.__commitmentManager.getCommitments()
                        if not commits == -1:
                            for x in commits.queue:
                                #print("COMMITMENT TYPE: ", x.getCommitmentType())
                                if x.getCommitmentType() == CommitmentTypes.TRAIN:
                                    self.__training.train()
                                    self.__nextState=States.EVALUATION
                                    self.__sleepEvent.wait(randint(3,10))
                                    print("AGGREGATORCHECK : " , self.__knowledgebase.getAggregator())
                                    if(self.__knowledgebase.getAggregator()==None):
                                        self.__knowledgebase.setAggregator((self.__ip, self.__port))
                                        for adress in self.__contacts:
                                            if(not adress==(self.__ip, self.__port)):
                                                message=Message((self.__ip, self.__port),
                                                                (adress[0], adress[1]),
                                                                MessageTypes.INFORM,
                                                                "Aggregator",
                                                                "")
                                                self.__communication.sendMessage(message)
                                        commitment=Commitment((self.__ip, self.__port),
                                                            (self.__ip, self.__port),
                                                            CommitmentTypes.AGGREGATE,
                                                            0)
                                        self.__commitmentManager.addCommitment(commitment)
                                        #self.__knowledgebase.setAggregator((self.__ip, self.__port))
                                    else:
                                        aggregator=self.__knowledgebase.getAggregator()
                                        commitment=Commitment((self.__ip, self.__port),
                                                            aggregator,
                                                            CommitmentTypes.SHARE,
                                                            "Aggregated_model")
                                        self.__commitmentManager.addCommitment(commitment)
                                    break

                    case 5: #Evaluate (select from 3 modes ?)
                        print(self.__port," :state: ", info)
                        self.__evaluation.resetCollectedWeights()
                        #print(self.__port, " :COLLECTED WEIGHTS RESET")
                        commits = self.__commitmentManager.getCommitments()
                        for x in commits.queue:
                            #Receive Model
                            if x.getCommitmentType() == CommitmentTypes.AGGREGATE:
                                self.__sleepEvent.wait(10)
                                nrWeights = len(self.__knowledgebase.getMembers())
                                #print(self.__port," :nrWeights: ", nrWeights)
                                #print(self.__port," :len of collectedWeights: ", len(self.__evaluation.getCollectedWeights()))
                                print(self.__port , ":WEIGHTS NEEDED FOR AGG: ", nrWeights)
                                while len(self.__evaluation.getCollectedWeights())<nrWeights:
                                    print(self.__port, " :COLLECTED WEIGHTS IN AGG: ",len(self.__evaluation.getCollectedWeights()))
                                    self.__sleepEvent.wait(10)
                                    pass
                                #print(self.__port," :passed while-loop")
                                print(self.__port," :Collected Weights equal to nr of sharing clients: ", len(self.__evaluation.getCollectedWeights()), " = ", nrWeights)
                                avgW = self.__evaluation.averageWeight(self.__evaluation.getCollectedWeights())
                                self.__training.setWeights(avgW)
                                print(self.__port," :AGGREGATED WEIGHTS SET")
                                #Send agg model
                                for adress in self.__knowledgebase.getMembers():
                                    message = Message((self.__ip,self.__port),
                                                      adress,
                                                      MessageTypes.INFORM, 
                                                      "Weight",
                                                      self.__training.getWeights())
                                    self.__communication.sendMessage(message)
                                print(self.__port," :AGGREGATED WEIGHTS SENT")
                                #self.__nextState=States.REWARDING
                                break
                            elif x.getCommitmentType() == CommitmentTypes.SHARE:
                                adress = self.__knowledgebase.getAggregator()
                                message = Message((self.__ip, self.__port),
                                                  adress,
                                                  MessageTypes.INFORM, 
                                                  "Weight", 
                                                  self.__training.getWeights())
                                self.__communication.sendMessage(message)
                                print(self.__port," :WEIGHTS SENT TO: ", adress)
                                #flag here to receive and eval model!
                                while len(self.__evaluation.getCollectedWeights())<1:
                                    pass
                                avgW = self.__evaluation.averageWeight(self.__evaluation.getCollectedWeights())
                                self.__training.setWeights(avgW)
                                print(self.__port," :AGGREGATED WEIGHTS RECEIVED AND SET")
                                self.__training.evaluate()
                                #self.__registered.clear()
                                #self.__registered.wait()
                                #set weights + eval here
                                break
                        self.__nextState=States.REWARDING
                    
                    case 6: #Reward participants
                        print(self.__port," :state: ", info)
                        commitments=self.__commitmentManager.getCommitments()
                        while(not commitments.empty()):
                            commitment=commitments.get()
                            if(commitment.getCreditor==(self.__ip, self.__port)):
                                message=Message((self.__ip, self.__port),
                                                commitment.getDebtor(),
                                                MessageTypes.INFORM,
                                                "Reward",
                                                commitment.getReward())
                                self.__communication.sendMessage(message)
                        self.reset()
                        self.__nextState=States.DISCOVERY

                self.__currentState=self.__nextState

    def reset(self):
        self.__negotiation.reset()
        self.__knowledgebase.resetFederation()
        self.__commitmentManager.reset()

    def __init__(self,
                 ip,
                 port_comm,
                 ipCatalog,
                 portCatalog,
                 objective,
                 modelInfo,
                 modelAccuracy,
                 modelLoss,
                 datasetInfo,
                 patience,
                 costLimit,
                 price): #Set to price = 0.0 for test
        self.__commitmentManager=CommitmentManager(port_comm)
        self.__profileManager=ProfileManager(ip, port_comm, objective, modelInfo, modelAccuracy, modelLoss, datasetInfo, price)
        self.__communication=Communication(ip, port_comm, self)
        self.__evaluation=Evaluation()
        self.__negotiation=Negotiation(self, ip, port_comm)
        self.__ruleEngine=RuleEngine(patience, costLimit, price)
        self.__knowledgebase=KnowledgeBase("","")
        

        self.__ipCatalog=ipCatalog
        self.__portCatalog=portCatalog
        self.__ip=ip
        self.__port=port_comm
        self.__contacts=list()
        self.clientId = self.__port

        self.__training=Training(self.clientId)

        self.__sleepEvent=threading.Event()
        self.__registered=threading.Event()
        self.__discovered=threading.Event()
        self.__beginNegotiation=threading.Event()
        

        self.__currentState=States.REGISTRATION
        self.__nextState=States.REGISTRATION

        print("starting agent FSM listening at: ", self.__communication.getIp(), ";", self.__communication.getPort())
        threading.Thread.__init__(self)
        self.start()

    


