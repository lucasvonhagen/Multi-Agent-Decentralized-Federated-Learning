

class Federation():
    def getMembers(self):
        return self.__members

    def addMember(self, member):
        self.__members.append(member)

    def setAggregator(self, aggregator):
        self.__aggregator=aggregator

    def getAggregator(self):
        return self.__aggregator

    def __init__(self):
        self.__members=list()
        self.__aggregator=None
