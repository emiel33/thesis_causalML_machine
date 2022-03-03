 
from cmath import e, exp
import numpy as np
import maintenance


class Machine:
   
    def __init__(self,machineParameters):
         
         
         self.condition = machineParameters[0]
         self.criticalDamage = machineParameters[1]
         self.betas = machineParameters[2]
         self.sigma = machineParameters[3]
         self.scaleParameter = machineParameters[4]
         
         
        
    
    def failed(self):
        if(self.condition > self.criticalDamage):
             return True
        return False
    
    # linearily interpolate the changes of covariates between points
    # change the speed of time as a proxy for accelerated wear i.e.
    # under additive accumulation of damage each time instance the machine can get damaged a bit further than time would indicate, this adds up
    # The damage acts multiplicatively over the covariates
    def scaledTimeIncrement(self,prevCovariates,covariates,Betas,stepsize):
        return ((e**(np.dot(Betas,prevCovariates)))+(e**(np.dot(Betas,covariates))))*stepsize/2

    def meanDegradation(self,alpha,slope = 1):
        return slope * alpha**2
     #denominator causes issues ! have to look into this!                                                                                                                   
    def shapeFunction(self,alpha,prevalpha):
        return (self.meanDegradation(alpha) - self.meanDegradation(prevalpha))


class Deteriorationprocess:

    def __init__(self, processArguments, machine, covariates,maintenance):
       
        # define basic process properties
        self.timeFrame = processArguments[0]
        self.steps = processArguments[1]
        self.stepsize = self.timeFrame/self.steps
        
        # define machine and it's properties tied to the process
        self.machine =  machine

        # create dictionary to store the condition over time
        self.conditionArray = np.empty(self.steps)
        self.treatmentDecisionArray = np.empty(self.steps)
       
        # import exogenous covariates array into the process
        self.covariates = covariates

        # define treatment Policy

        self.maintenance = maintenance


    # alpha is the parameter that determines the mean deterioration! We assume constancy of all covariates over the period until the current!

    def generaterun(self):
     # define dictionary for condition values at given time intervals
       
        self.conditionArray[0] = 0
        self.treatmentDecisionArray[0] = 0
        prevAlpha = 0
    
        
        for step in range(1,self.steps):
             
             failedstate = self.machine.failed()
             if(failedstate == True):
                self.conditionArray[step] = 0
                continue

             

             # update cumulative alpha , take step - 1 since influence over the past period has been determined by covariates at step - 1
             #i.e. in case of the first step 1 determined by the covariates at time 0
             currentAlpha = prevAlpha + self.machine.scaledTimeIncrement(self.covariates[step-1],self.covariates[step],self.machine.betas,self.stepsize)
            
             
             shape = self.machine.shapeFunction(currentAlpha,prevAlpha)
             
             incrementDeterioriation =np.random.gamma(shape, self.machine.scaleParameter)
             self.conditionArray[step] = self.conditionArray[step-1] + incrementDeterioriation
             self.machine.condition = self.conditionArray[step]

             self.treatmentDecisionArray[step] = self.maintenance.generateTreatmentDecision(self.covariates[step])

             if(self.treatmentDecisionArray[step] == 1):
               self.conditionArray[step] = self.maintenance.performTreatment(self.conditionArray[step])
             
             
             
             
             # set prevAlpha to current Alpha for next iteration
             prevAlpha = currentAlpha
         

        return self.conditionArray, self.treatmentDecisionArray







# m(t) in paper, determines normal degradation profile i.e. the amount of shocks in 1 jump/ timesteps.
# The scale parameter is left as default 1


# under assumption that covariates remain constant until next measurement:

  

'''
    


'''