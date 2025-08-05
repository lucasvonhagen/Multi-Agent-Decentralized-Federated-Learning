
import Commitment
import queue


#Current commitment, list of all accepted commitments
class CommitmentManager:

    def __init__(self, clientId):
        self.__commitments=queue.Queue()
        self.__completedCommitments=queue.Queue()
        self.__pendingCommitments=queue.Queue()
        self.clientId = clientId

    def reset(self):
        self.__commitments=queue.Queue()
        self.__completedCommitments=queue.Queue()
        self.__pendingCommitments=queue.Queue()

    def addCommitmentForEvaluation(self, commitment):
        self.__pendingCommitments.put(commitment)

    def addCommitment(self, commitment):
        #print(self.clientId , " :added commitment: ", commitment.getCommitmentType().name)
        self.__commitments.put(commitment)

    def setCommitments(self, commitments):
        self.__commitments=commitments

    def getCompletedCommitment(self):
        if not self.__completedCommitments.empty():
            return self.__completedCommitments.get()
        else:
            return -1

    def getCommitmentForEvaluation(self):
        if not self.__pendingCommitments.empty():
            return self.__pendingCommitments.get()
        else:
            return -1
        

    #return -1 if all commitments completed
    def getCommitments(self):
        if not self.__commitments.empty():
            return self.__commitments
        else:
            return -1
        
    
        