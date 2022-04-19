
import numpy as np
from cmath import e

class Machine:
   
    def __init__(self,machineParameters):
         
         # initialize parameters for machine

         self.initialCondition = machineParameters[0]
         self.criticalDamage = machineParameters[1]
         self.betas = machineParameters[2]
         self.sigma = machineParameters[3]
         self.maxProductionSpeed = machineParameters[4]
        
    # failurecondition check for the machine

    def failed(self,condition):
        if(condition >= self.criticalDamage):
             return True
        return False

    # defines the expected degradation step for the next turn!
    # For the moment chosen to be linear
    
    def meanDegradation(self,alpha,slope = 100):
        return slope * alpha
    


    

    
    
    
