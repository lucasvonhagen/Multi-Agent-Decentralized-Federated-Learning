#evaluation of training/federation/model. maybe out-of-scope?
import tensorflow as tf


class Evaluation:

    def __init__(self):
        self.collectedWeights = []


    #Obsolete, use function in Training module
    def evaluateModel(self):
        print("Conducting Evaluation")
        self.test_loss, self.test_accuracy = self.model.evaluate(self.test_images, self.test_labels, verbose = 0)
        return self.test_loss, self.test_accuracy
        
    def collectWeights(self,weights):
        self.collectedWeights.append(weights)
        return self.collectedWeights

    def averageWeight(self, collectedWeights):
        avg_weights = []
        for weights in zip(*collectedWeights):
            avg_weights.append(tf.reduce_mean(weights, axis=0))
        return avg_weights

    def Aggregate(self,avg_weights):
        self.model.set_weights(avg_weights)

    def getCollectedWeights(self):
        return self.collectedWeights
    
    def resetCollectedWeights(self):
        del self.collectedWeights[:]

    

