from AgentProfile import AgentProfile

#Ändra till current profile, getProfile
class ProfileManager:

    def __init__(self, ip, port, objective, modelInfo, modelAccuracy, modelLoss, datasetInfo, price):
        self.__currentProfile=AgentProfile(ip, port, objective, modelInfo, modelAccuracy, modelLoss, datasetInfo, price)
        
    def getCurrentProfile(self):
        return self.__currentProfile
    
    def getObjective(self):
        return self.__currentProfile.getObjective()
    
    def getModelAccuracy(self):
        return self.__currentProfile.getModelAccuracy()
    
    def getModelLoss(self):
        return self.__currentProfile.getModelLoss()
    
    def getModelInfo(self):
        return self.__currentProfile.getModelInfo()
    
    def getDatasetInfo(self):
        return self.__currentProfile.getDatasetInfo()
    
    def getPrice(self):
        return self.__currentProfile.getPrice()
    
    def setAccuray(self, accuracy):
        self.__currentProfile.setAccuracy(accuracy)

    def setLoss(self, loss):
        self.__currentProfile.setLoss(loss)

