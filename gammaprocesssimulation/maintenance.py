

# sigmoid helper function
from calendar import c
import numpy as np
from math import e
import random as rand

class MaintenanceProgram:

    def __init__(self,processArguments,generationArguments,rng, treatmentplan = "policy"):
        
        self.mean = generationArguments[0]
        self.steps = processArguments[1]
        self.startTreatmentPlan = processArguments[4]
        self.endTreatmentPlan = processArguments[5]
        self.standarddevs = generationArguments[1]
        self.policy =  self.generateNormalTreatmentPolicy()
        self.rng = rng
        self.treatmentPlan = treatmentplan
        
    def generateRandomTreatmentPlan(self):
        plan = list()
        for step in (self.steps -self.startPrediction):
            plan.append(rand.randint(0,1))

        self.treatmentPlan = plan



    def generateNormalTreatmentPolicy(self):
        length = len(self.mean)
        policy = np.array([0.001,0.001,0.001])
    
        return policy

    def sigmoid(self,x):
        return 1/(1 + np.exp(x))

        # draw treatment with probability sigmoid of covariates ? this is not normalized, does 
    def generateTreatmentDecision(self,covariates,step): 
        
        
        
        if(self.treatmentPlan == "policy" or step < self.startTreatmentPlan or step > self.endTreatmentPlan):
            # if more than 1 than the data is quite rare, and could indicate repair is necessary
            standardizedData= ( np.array(covariates)- np.array(self.mean))/ np.array(self.standarddevs)
            sigmoidArg= np.dot(self.policy,standardizedData)
            maintenance = self.rng.binomial(1,self.sigmoid(sigmoidArg))
        
        elif( self.treatmentPlan == "random"):
            maintenance = rand.randint(0,1)
        else: 
            # follow the predefined treatmentPlan from the first predictionday !
            print(step)
            print("ldlfjqsdlfk")
            print(self.treatmentPlan[step - self.startTreatmentPlan])
            maintenance = self.treatmentPlan[step - self.startTreatmentPlan]
           
       
        return maintenance
    
    def setTreatmentPlan(self, treatmentPlan = None):
            self.treatmentPlan == treatmentPlan


    def calculateTreatmentCost(self):

        productionReductionFactor = 0.5
        return productionReductionFactor
   
    def performTreatment(self,preRepairMachineTime,preRepairGammaState,currentCovariates,machine,history):
       
       # For the purposes of this simulation repair success depends on the current and previous period covariates
        '''
        if(len(history) < 1):
            temperatureInfluence = (currentCovariates[0])*0.8
            usageInfluence = (currentCovariates[1])*1.3
            humidity = (currentCovariates[2])*1
        else:
            temperatureInfluence = (currentCovariates[0]+ history[-1][2]*0.5)*1
            usageInfluence = (currentCovariates[1] + history[-1][3]*0.5)*1.5
            humidity = (currentCovariates[2] + history[-1][4]*0.5)*1.2
        '''
        # check correctness
        postRepairGammaState  =  (preRepairGammaState - self.rng.lognormal(3,0.10)/machine.sigma**2)
       # Machine time reset to earlier point / chosen to be lower than the average would suspect in able to indicate incomplete revearsal 
       # if machine had exponential decay this would make early intervention better, in linear case less important!
        newMachineTime =  (machine.machineTime(postRepairGammaState) + preRepairMachineTime)/2

        if (postRepairGammaState < 0):
            postRepairGammaState = 0
        
        return  newMachineTime, postRepairGammaState , preRepairGammaState
