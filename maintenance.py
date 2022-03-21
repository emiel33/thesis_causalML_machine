

# sigmoid helper function
import numpy as np

class MaintenanceProgram:

    def __init__(self,productionQuote,generationArguments):
        self.mean = generationArguments[0]
        self.standarddevs = generationArguments[1]
        self.productionQuote = productionQuote
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
        

        # if more than 1 than the data is quite rare, and could indicate repair is necessary
        standardizedData= ( np.array(covariates)- np.array(self.mean))/ np.array(self.standarddevs)
        sigmoidArg= np.dot(self.policy,standardizedData)
        maintenance = np.random.binomial(1,self.sigmoid(sigmoidArg))
       
        return maintenance

    def calculateTreatementCost(self):

        productionReductionFactor = 0.2
        return productionReductionFactor
   
    def performTreatment(self,currentCondition):
        newCondition = currentCondition - np.random.normal(5,2.5)
        if(newCondition<0):
            newCondition = 0
        return  newCondition
