

# sigmoid helper function
import numpy as np

class MaintenanceAction:

    def __init__(self,mean,standarddevs):
        self.mean = mean
        self.standarddevs = standarddevs
        self.policy =  self.__defineTreatmentPolicy()
        
        


    def __defineTreatmentPolicy(self):
        length = len(self.mean)
        policy = np.empty(length)
        for i in range(length):
            policy[i] = np.random.uniform(1/length)
    
        return policy

    def sigmoid(self,x):
        return 1/(1 + np.exp(x))

        # draw treatment with probability sigmoid of covariates ? this is not normalized, does 
    def generateTreatmentDecision(self,covariates): 
        
       
        standardizedData= ( np.array(covariates) - np.array(self.mean))/ np.array(self.standarddevs)
        
        sigmoidArg= np.dot(self.policy,standardizedData)
        return np.random.binomial(1,self.sigmoid(sigmoidArg))
   
    def performTreatment(self,currentCondition):
        return currentCondition - np.random.normal(10,5)