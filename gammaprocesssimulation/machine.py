
import numpy as np
from cmath import e

class Machine:
   
    count = 0
    
   

    def __init__(self,rng):
        self.initialCondition,self.criticalDamage,self.betas,self.sigma,self.maxProductionSpeed = self.__generateRandomParameters(rng)
        Machine.count+=1
        self.caseNumber = Machine.count

    # failurecondition check for the machine

    def failed(self,condition):
        if(condition >= self.criticalDamage):
             return True
        else:
             return False

    def __generateRandomParameters(self,rng):
        
        initialCondition = 0
        criticalDamage = rng.normal(2000,50)
        betas = [rng.normal(0.2/10,0.002),rng.normal(0.5/5,0.002),rng.normal(0.3/20,0.002)]
        sigma = rng.normal(3,0.5)
        maxProductionSpeed = 100

        return initialCondition,criticalDamage,betas,sigma,maxProductionSpeed
    
    def setParameters(self,machineParameters):
         
        # initialize parameters for machine
         
        self.initialCondition = machineParameters[0]
        self.criticalDamage = machineParameters[1]
        self.betas = machineParameters[2]
        self.sigma = machineParameters[3]
        self.maxProductionSpeed = machineParameters[4]
        
        

    # defines the expected degradation step for the next turn!
    # For the moment chosen to be linear
    
    def meanDegradation(self,machineTime,slope = 100):
        return slope * machineTime

    def machineTime(self,degradation, slope = 100):
        return degradation/slope
    
    def getParameters(self):
        return [self.caseNumber,self.initialCondition,self.criticalDamage,self.betas,self.sigma,self.maxProductionSpeed]


    

    
    
    
