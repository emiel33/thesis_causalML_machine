

# sigmoid helper function
from calendar import c
import numpy as np
from math import e

class MaintenanceProgram:

    def __init__(self,generationArguments,rng):
        self.mean = generationArguments[0]
        self.standarddevs = generationArguments[1]
        self.policy =  self.__defineTreatmentPolicy()
        self.rng = rng
        


    def __defineTreatmentPolicy(self):
        length = len(self.mean)
        policy = np.array([0.2,0.1,0.2])
    
        return policy

    def sigmoid(self,x):
        return 1/(1 + np.exp(x))

        # draw treatment with probability sigmoid of covariates ? this is not normalized, does 
    def generateTreatmentDecision(self,covariates): 
        

        # if more than 1 than the data is quite rare, and could indicate repair is necessary
        standardizedData= ( np.array(covariates)- np.array(self.mean))/ np.array(self.standarddevs)
        sigmoidArg= np.dot(self.policy,standardizedData)
        maintenance = self.rng.binomial(1,self.sigmoid(sigmoidArg))
       
        return maintenance

    def calculateTreatementCost(self):

        productionReductionFactor = 0.5
        return productionReductionFactor
   
    def performTreatment(self,currentMachineTime,currentGammaState,currentCovariates,machine,history):
       
       # For the purposes of this simulation repair success depends on the current and previous period covariates
        
        if(len(history) < 1):
            temperatureInfluence = (currentCovariates[0])*0.8
            usageInfluence = (currentCovariates[1])*1.3
            humidity = (currentCovariates[2])*1
        else:
            temperatureInfluence = (currentCovariates[0]+ history[-1][2]*0.5)*1
            usageInfluence = (currentCovariates[1] + history[-1][3]*0.5)*1.5
            humidity = (currentCovariates[2] + history[-1][4]*0.5)*1.2
        
        newGammaState  =  currentGammaState - self.rng.normal(temperatureInfluence + usageInfluence + humidity,5)/machine.sigma**2
       # Machine time reset to earlier point / chosen to be lower than the average would suspect in able to indicate incomplete revearsal 
       # if machine had exponential decay this would make early intervention better, in linear case less important!
        newMachineTime =  (machine.machineTime(newGammaState) + currentMachineTime)/2

        if (newGammaState < 0):
            newGammaState = 0
        
        return  newMachineTime, newGammaState
