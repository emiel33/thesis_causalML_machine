from cmath import e, exp
import numpy as np

from maintenance import MaintenanceProgram
from array import *

class Deteriorationprocess:

    count = 0

    def __init__(self, processArguments, machine, covariateGenerator ,maintenanceProgram,rng):
       
        # update static cound and caseNumber
        Deteriorationprocess.count+=1
        self.caseNumber = Deteriorationprocess.count

        # define basic process properties
        self.timeFrame = processArguments[0]
        self.steps = processArguments[1]
        self.scaleParameter = processArguments[2]
        self.stepsize = self.timeFrame/self.steps
        self.decisiondelta = processArguments[3]
        
        # define machine and it's properties tied to the process
        
        self.machine =  machine
        self.covariateGenerator = covariateGenerator
        self.maintenance = maintenanceProgram

        # define random number generator
        self.rng = rng

    # increment the machinetime
    def scaledTimeIncrement(self,covariates,Betas)
        # choose exponential time step
        return (e**(np.dot(Betas,covariates)))*self.stepsize
    
     
    # creating equivalent to "z"-values for gamma distribution!                                                                                                                 
    def shapeFunction(self,newMachineTime,oldMachineTime):
        # why new - old mean?
        return (self.machine.meanDegradation(newMachineTime) - self.machine.meanDegradation(oldMachineTime))/ self.machine.sigma**2
   
    def generaterun(self):
        
        history = list()
        oldMachineTime = 0 # ?
        prevGammaState = self.machine.initialCondition # 0?
        prevDegradation = prevGammaState*self.machine.sigma**2 # Z(t) = gamma * sigma^2
        currentDegradation = 0 # initial condition?

        for step in range(self.steps): # 50 times:
             
             # check if machine has failed?
            if(self.machine.failed(currentDegradation)): # if > dan breakdown treshold:

              # if failed:
              timeStepData = [self.machine.caseNumber,step,None,None,None,None,None,None,None] # ?
              history.append(timeStepData)

            else:
             # if not failed:
             # generate covariates at for current step

             # why next step?
             currentCovariates = self.covariateGenerator.generateCovariateTimePoint()
             
             # increment machineTime according to theory of accumulation of damages
             # machinetime? leg dit meer uit in paper mss
             newMachineTime = oldMachineTime + self.scaledTimeIncrement(currentCovariates, self.machine.betas)
             
             # determine shape parameter of gamma jump!
             shape = self.shapeFunction(newMachineTime,oldMachineTime)

             # jump the deterioration state!
             # Z(t)
             incrementDeterioriation = self.rng.gamma(shape, self.scaleParameter)
             currentGammaState = prevGammaState + incrementDeterioriation
             currentDegradation = currentGammaState * self.machine.sigma**2 # Z(t) = gamma(t) * sigma^2

             # check if machine hs broken down (current degradation > critical degradation)
             if(currentDegradation >= self.machine.criticalDamage):
                 currentDegradation == self.machine.criticalDamage
                 

             # calculate Production for the period given current condition

             treatmentDecision = self.maintenance.generateTreatmentDecision(currentCovariates, step)
            

             if(treatmentDecision):
                 # return new MachineTime , adjust the currentGammaState and set preRepairGammaState to the previously calculated currentGammaState
              newMachineTime,postRepairGammaState,preRepairGammaState =  self.maintenance.performTreatment(newMachineTime,currentGammaState,currentCovariates,self.machine,history)
              currentGammaState = postRepairGammaState
              currentDegradation = currentGammaState *self.machine.sigma**2
              preRepairDegradation = preRepairGammaState * self.machine.sigma**2
              repairEffect = currentDegradation - preRepairDegradation
              currentProduction = (1 - currentDegradation/self.machine.criticalDamage)*self.machine.maxProductionSpeed*self.stepsize*self.maintenance.calculateTreatmentCost()
             else:
               # calculate production under no treatment condition
               # relation between deteriation and production
              currentProduction = (1 - currentDegradation/self.machine.criticalDamage)*self.machine.maxProductionSpeed*self.stepsize
              repairEffect = None
             
             
             
             timestepData = [self.caseNumber,step, currentCovariates[0],currentCovariates[1],currentCovariates[2],currentDegradation,repairEffect,currentProduction,treatmentDecision]
             history.append(timestepData)

             

             
            # set current values to old values for next iteration
             
             oldMachineTime = newMachineTime
             prevGammaState = currentGammaState
             prevDegradation = prevGammaState*self.machine.sigma**2
         

        return history







# m(t) in paper, determines normal degradation profile i.e. the amount of shocks in 1 jump/ timesteps.
# The scale parameter is left as default 1


# under assumption that covariates remain constant until next measurement:

  
