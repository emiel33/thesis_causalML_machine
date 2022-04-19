 
from cmath import e, exp
import numpy as np
from maintenance import MaintenanceProgram
from array import *



class Deteriorationprocess:

    def __init__(self, processArguments, machine, covariateGenerator ,maintenanceProgram):
       
        # define basic process properties
        self.timeFrame = processArguments[0]
        self.steps = processArguments[1]
        self.scaleParameter = processArguments[2]
        self.stepsize = self.timeFrame/self.steps
        
        # define machine and it's properties tied to the process
        
        self.machine =  machine
        self.covariateGenerator = covariateGenerator
        self.maintenance = maintenanceProgram

    # increment the machinetime
    def scaledTimeIncrement(self,covariates,Betas):
        return (e**(np.dot(Betas,covariates)))*self.stepsize
    
     
    # creating equivalent to "z"-values for gamma distribution!                                                                                                                 
    def shapeFunction(self,newMachineTime,oldMachineTime):
        return (self.machine.meanDegradation(newMachineTime) - self.machine.meanDegradation(oldMachineTime))/ self.machine.sigma**2
   
    def generaterun(self):
        
        dataList = list()
        oldMachineTime = 0
        prevGammaState= float(self.machine.initialCondition)
        prevDegradation = prevGammaState* self.machine.sigma**2
        
       
        
        


        for step in range(self.steps):
             
             

             # generate covariates at for current step
             covariates = self.covariateGenerator.generateCovariateTimePoint()
             
             # increment machineTime according to theory of accumulation of damages
             newMachineTime = oldMachineTime + self.scaledTimeIncrement(covariates, self.machine.betas)
             
             # determine shape parameter of gamma jump!
             shape = self.shapeFunction(newMachineTime,oldMachineTime)
             
             # jump the deterioration state!
             incrementDeterioriation = np.random.gamma(shape, self.scaleParameter)
             print(type(prevGammaState))
             print(type(incrementDeterioriation))
             print(step)
             currentGammaState = prevGammaState + incrementDeterioriation
             currentDegradation = currentGammaState * self.machine.sigma**2
             
             # calculate sensor output as proxy for condition
             sensordata = np.random.normal(currentDegradation,10)
             
             # calculate Production for the period given current condition

             production = (self.machine.criticalDamage - (currentDegradation + prevDegradation)/2)*self.machine.maxProductionSpeed*self.stepsize*self.maintenance.calculateTreatementCost()

             treatmentDecision = self.maintenance.generateTreatmentDecision(covariates)
                    
             if(treatmentDecision):
              newMachineTime,currentGammaState = self.maintenance.performTreatment(newMachineTime,currentGammaState)
             
             
             timestepData = [step, covariates[0],covariates[1],covariates[2],sensordata,currentDegradation,production,treatmentDecision]
             dataList.append(timestepData)

             # check if machine has failed?

             failedstate = self.machine.failed(currentDegradation)
             
             if(failedstate == True):
                self.machine.condition = np.nan
                continue
             
             # set current values to old values for next iteration
             
             oldMachineTime = newMachineTime
             prevGammaState = currentGammaState
             prevDegradation = prevGammaState*self.machine.sigma**2
         

        return dataList







# m(t) in paper, determines normal degradation profile i.e. the amount of shocks in 1 jump/ timesteps.
# The scale parameter is left as default 1


# under assumption that covariates remain constant until next measurement:

  
