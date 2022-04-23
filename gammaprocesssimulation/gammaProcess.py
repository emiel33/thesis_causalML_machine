 
from cmath import e, exp
import numpy as np

from maintenance import MaintenanceProgram
from array import *



class Deteriorationprocess:

    def __init__(self, processArguments, machine, covariateGenerator ,maintenanceProgram,rng):
       
        # define basic process properties
        self.timeFrame = processArguments[0]
        self.steps = processArguments[1]
        self.scaleParameter = processArguments[2]
        self.stepsize = self.timeFrame/self.steps
        
        # define machine and it's properties tied to the process
        
        self.machine =  machine
        self.covariateGenerator = covariateGenerator
        self.maintenance = maintenanceProgram

        # define random number generator
        self.rng = rng

    # increment the machinetime
    def scaledTimeIncrement(self,covariates,Betas):
        return (e**(np.dot(Betas,covariates)))*self.stepsize
    
     
    # creating equivalent to "z"-values for gamma distribution!                                                                                                                 
    def shapeFunction(self,newMachineTime,oldMachineTime):
        return (self.machine.meanDegradation(newMachineTime) - self.machine.meanDegradation(oldMachineTime))/ self.machine.sigma**2
   
    def generaterun(self):
        
        history = list()
        oldMachineTime = 0
        prevGammaState= float(self.machine.initialCondition)
        prevDegradation = prevGammaState* self.machine.sigma**2
        currentDegradation = 0
        
       
        
        


        for step in range(self.steps):
             
             # check if machine has failed?

            if(self.machine.failed(currentDegradation)):
                
               timeStepData = [self.machine.caseNumber,step,None,None,None,None,None,None,None]
               history.append(timeStepData)

            else:
             
             # generate covariates at for current step
             currentCovariates = self.covariateGenerator.generateCovariateTimePoint()
             
             # increment machineTime according to theory of accumulation of damages
             newMachineTime = oldMachineTime + self.scaledTimeIncrement(currentCovariates, self.machine.betas)
             
             # determine shape parameter of gamma jump!
             shape = self.shapeFunction(newMachineTime,oldMachineTime)
             
             # jump the deterioration state!
             incrementDeterioriation = self.rng.gamma(shape, self.scaleParameter)
             currentGammaState = prevGammaState + incrementDeterioriation
             currentDegradation = currentGammaState * self.machine.sigma**2
             
             # calculate sensor output as proxy for condition
             sensordata =  self.rng.normal(currentDegradation,10)
             
             # calculate Production for the period given current condition

             currentProduction =  max(0,(self.machine.criticalDamage - (currentDegradation + prevDegradation)/2)*self.machine.maxProductionSpeed*self.stepsize*self.maintenance.calculateTreatementCost())

             treatmentDecision = self.maintenance.generateTreatmentDecision(currentCovariates)
                    
             if(treatmentDecision):
              newMachineTime,currentGammaState = self.maintenance.performTreatment(newMachineTime,currentGammaState,currentCovariates,self.machine,history)
             
              
             
             
             
             timestepData = [self.machine.caseNumber,step, currentCovariates[0],currentCovariates[1],currentCovariates[2],sensordata,currentDegradation,currentProduction,treatmentDecision]
             history.append(timestepData)

             

             
            # set current values to old values for next iteration
             
             oldMachineTime = newMachineTime
             prevGammaState = currentGammaState
             prevDegradation = prevGammaState*self.machine.sigma**2
         

        return history







# m(t) in paper, determines normal degradation profile i.e. the amount of shocks in 1 jump/ timesteps.
# The scale parameter is left as default 1


# under assumption that covariates remain constant until next measurement:

  
