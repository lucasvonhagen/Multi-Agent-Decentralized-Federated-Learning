#model + dataset
from Federation import Federation

class KnowledgeBase:
    def __init__(self, model, dataset):
        self.__model=model
        self.__dataset=dataset
        self.__federation=Federation()

    def setModel(self, model):
        self.__model=model

    def getModel(self):
        return self.__model
    
    def getData(self):
        return self.__dataset
    
    def getMembers(self):
        return self.__federation.getMembers()

    def addMember(self, member):
        self.__federation.addMember(member)
        print("registered from federation: ", self.__federation.getMembers())
        print("Aggregator: ", self.__federation.getAggregator())

    def setAggregator(self, aggregator):
        self.__federation.setAggregator(aggregator)
        print("aggregator set!: ", self.__federation.getAggregator())

    def getAggregator(self):
        return self.__federation.getAggregator()
    
    def resetFederation(self):
        self.__federation=Federation()