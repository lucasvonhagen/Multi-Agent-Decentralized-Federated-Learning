

class RuleEngine:

    #Negotiation rounds to reach limit, costLimit (upper bound if objetive=TRAINING, lower bound if objective=PROFIT), price to train (if objective=PROFIT)
    def __init__(self, patience, costLimit, price=0.0):
        self.__patience=patience
        self.__costLimit=costLimit
        self.__price=price

    def getPatience(self):
        return self.__patience
    
    def getCostLimit(self):
        return self.__costLimit
    
    def getPrice(self):
        return self.__price
    
    def setCostLimit(self, costLimit):
        self.__patience=costLimit