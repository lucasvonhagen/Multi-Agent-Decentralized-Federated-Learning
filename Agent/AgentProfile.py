
class AgentProfile():

    def __init__(self, ip, port, objective, modelInfo, modelAccuracy, modelLOss, datasetInfo, price):
        self.__ip=ip
        self.__port=port
        self.__objective=objective
        self.__modelInfo=modelInfo
        self.__modelAccuracy=modelAccuracy
        self.__modelLoss=modelLOss
        self.__datasetInfo=datasetInfo
        self.__price=price

    def getIp(self):
        return self.__ip
    
    def getPort(self):
        return self.__port
    
    def getObjective(self):
        return self.__objective
    
    def getModelInfo(self):
        return self.__modelInfo
    
    def getModelAccuracy(self):
        return self.__modelAccuracy
    
    def getModelLoss(self):
        return self.__modelLoss
    
    def getDatasetInfo(self):
        return self.__datasetInfo
    
    def getPrice(self):
        return self.__price
    
    def setAccuracy(self, accuracy):
        self.__modelAccuracy=accuracy

    def setLoss(self, loss):
        self.__modelLoss=loss


