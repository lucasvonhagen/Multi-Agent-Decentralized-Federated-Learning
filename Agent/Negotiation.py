

from Commitment import Commitment
from CommitmentTypes import CommitmentTypes
from ObjectiveTypes import ObjectiveTypes


#Class containing functions for negotiation between agents
class Negotiation:
    #idé: mappa (ip, port) : commitments[] för att hitta round num

    #returns false if decline, true if accept and new commit if re-negotiate
    def evaluateCommitment(self, objective, commitment, patience, costLimit, price=0.0):
        print(self.clientId , " :considering...")
        retVal=False #default return value
        debtor=commitment.getDebtor()
        creditor=commitment.getCreditor()
        commitmentType=commitment.getCommitmentType()
        reward=commitment.getReward()
        #add sender to negotiations if absent and put proposal in list:
        self.addToNegotiations(commitment)
        #evaluate received commitment:
        match objective:

            #profit oriented agent:
            case ObjectiveTypes.PROFIT:
                #acceptable price?
                if(commitmentType==CommitmentTypes.TRAIN and debtor==self.__adress):
                    pastProposals=self.__negotiations.get(creditor)
                    roundCurrent=len(pastProposals)
                    print(self.clientId , " :current negotiation round: ", roundCurrent)
                    #acceptable, atleast better than last offer and above lowest acceptable price:
                    if(reward>=pastProposals[roundCurrent-2].getReward() and reward >= costLimit):
                        retVal=True
                    #renegotiate if round <= maxRound:
                    else:
                        if(roundCurrent<=self.__roundMax and self.__controller.getCommitments()==-1):
                            rewardSuggestion=self.__profitReNegotiation(patience, costLimit, roundCurrent, price)
                            commitment=Commitment(debtor, creditor, commitmentType, rewardSuggestion)
                            retVal=commitment


            #improvement oriented agent:
            case ObjectiveTypes.IMPROVED_ACCURACY:
                #i want to train!
                if(commitmentType==CommitmentTypes.TRAIN and debtor==self.__adress):
                    retVal=True
                #acceptable price?
                elif(commitmentType==CommitmentTypes.TRAIN and creditor==self.__adress):
                    pastProposals=self.__negotiations.get(debtor)
                    roundCurrent=len(pastProposals)
                    #acceptable, atleast better than last offer and within budget:
                    if(reward<=pastProposals[roundCurrent-2].getReward() and reward <= costLimit):
                        retVal=True
                    #renegotiate if round <= maxRound:
                    else:
                        if(roundCurrent<=self.__roundMax):
                            rewardSuggestion=self.__improvementReNegotiation(patience, costLimit, roundCurrent)
                            commitment=Commitment(debtor, creditor, commitmentType, rewardSuggestion)
                            retVal=commitment
        return retVal


        
    #true if acceptable, else false (redundant?)
    def __profitEvaluation(self, type, debtor, creditor, reward, patience, costLimit, price):
        pass
    
    #true if acceptable, else false (redundant?)
    def __improvementEvaluation(self, type, debtor, creditor, reward, patience, costLimit, price):
        pass

    def __profitReNegotiation(self, patience, costLimit, roundCurrent, price):
        reward=price-(price-costLimit)*(roundCurrent/self.__roundMax)**patience
        return reward

    def __improvementReNegotiation(self, patience, costLimit, roundCurrent):
        reward=costLimit*(roundCurrent/self.__roundMax)**patience
        return reward

    def beginProposal(self, objective, sender, patience, price):
        print(self.clientId , " :initiating negotiation...")
        if(objective==ObjectiveTypes.PROFIT):
            retVal=Commitment(self.__adress,
                                  sender,
                                  CommitmentTypes.TRAIN,
                                  price)
        elif(objective==ObjectiveTypes.IMPROVED_ACCURACY):
            retVal=Commitment(sender,
                                  self.__adress,
                                  CommitmentTypes.TRAIN,
                                  price)
        return retVal
    
    def addToNegotiations(self, commitment):
        debtor=commitment.getDebtor()
        creditor=commitment.getCreditor()
        if(not debtor==self.__adress):
            self.__negotiations.setdefault(debtor, list()).append(commitment)
        elif(not creditor==self.__adress):
            self.__negotiations.setdefault(creditor, list()).append(commitment)

    def reset(self):
        self.__negotiations=dict()

    def __init__(self, controller, ip, port):
        self.__adress=(ip, port)
        self.__controller=controller
        self.__roundMax=50
        self.__negotiations=dict()
        self.clientId = port