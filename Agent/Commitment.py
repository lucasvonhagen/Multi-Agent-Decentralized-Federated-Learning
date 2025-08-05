#Commitment with type, responsibility and reward
class Commitment:
    
    def __init__(self, debtor, creditor, commitmentType, reward):
        self.__debtor=debtor
        self.__creditor=creditor
        self.__commitmentType=commitmentType
        self.__reward=reward

    def getDebtor(self):
        return self.__debtor
    
    def getCreditor(self):
        return self.__creditor
    
    def getCommitmentType(self):
        return self.__commitmentType
    
    def getReward(self):
        return self.__reward
