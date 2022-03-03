#%%
from cmath import e, exp
from this import d
from turtle import fd
from typing_extensions import Self
import numpy as np
import matplotlib.pyplot as plt



#generate covariance matrix to indicate relationship between covariates 

class CovariateGenerator:

    def __init__(self,processArguments,generationArguments):
        # general process parameters
        self.timeFrame = processArguments[0]
        self.steps = processArguments[1]
        self.stepsize = self.timeFrame/self.steps

        # parameters for exogenous variable generation
        self.mean = generationArguments[0]
        self.standarddev = generationArguments[1]

        self.covariance = self.__generateCovarianceMatrix()


    def __generateCovarianceMatrix(self):
    
        correlationMatrix = np.empty((len(self.standarddev),len(self.standarddev)))
        # generate standardized data i.e. correlation matrix and scale with standard deviations
        # no guarantee that it is positive definite! must be changed
        X = 0
        while X < len(self.standarddev):
         Y = 0
         while Y <= X:
            correlationMatrix[X][Y] = np.random.uniform(-0.5,0.5)
            correlationMatrix[Y][X] = correlationMatrix[X][Y]
            Y+=1
         X+=1
    
        standarddevMatrix = np.diag(self.standarddev)
        covariance = np.matmul(standarddevMatrix,np.matmul(correlationMatrix,standarddevMatrix))
        return covariance
    
    def generateCovariateTimePoint(self):
        
        # should we add bias here?
        covariates =  list(np.random.multivariate_normal(self.mean,self.covariance))
        
        return covariates
    
        # following combination ensures symmetry of the matrix,
        #return 0.5*(covariance + covariance.transpose()) as in paper bica 
    
    def generateCovariateTimeSeries(self):
        covariateTimeSeries = list()

       
        for step in range(self.steps):
            covariates = self.generateCovariateTimePoint()
            print(covariates)
            covariateTimeSeries.append(covariates)
            
            
        return covariateTimeSeries








'''
x, y = np.random.multivariate_normal([covariateGenerationArguments.get("temperature")[0],covariateGenerationArguments.get("temperature")[1]], covarianceMatrix, 5000)
plt.plot(x, y, 'x')
plt.axis('equal')
plt.show()
'''
# generate covariates based on the chosen mean and covariance matrix
# these covariates are not related to eachother in time!





'''
# momentarily no immediate relationship between covariates at differing time points


def generateSampleTimeSeries(generationArgs,covarianceMatrix,steps,samplesize):
    sample = []
    for case in range(samplesize):
        sample.extend(generateAttributeTimeSeries(case,generationArgs,covarianceMatrix,steps))

    return sample



# generate treatment vector given the observed characteristics using bernouli choice with sigmoid probability





'''



#%%












'''

class MaintenanceActions(Enum):

    upkeep = 1
    repair = 2
    overhaul = 3

class maintenance:
    
    criteria = []

    def __calculateCondition(condition,mean,stddev):
        
        newCondition = condition + np.random.normal(mean,stddev)
        return newCondition
    
    def __measureCondition(condition):
       return condition + np.random.normal(0,5)

    def maintenancePolicy(self,condition, covariates):
        if(self.__measureCondition(condition) + np.dot(self.criteria,covariates) < 20):
            return MaintenanceActions.upkeep
        if(self.__measureCondition(condition) + np.dot(self.criteria,covariates) < 20):
            return MaintenanceActions.repair
        if(self.__measureCondition(condition) + np.dot(self.criteria,covariates) < 20):
            return MaintenanceActions.overhaul
       
    
    
    def doMaintenance(self,condition,covariates):
        
        policy = self.maintenancePolicy(self,condition,covariates)

        if(policy == MaintenanceActions.upkeep):
            self.__calculateCondition(condition,10,5)
            print("Upkeep Performed")
       
        elif(policy == MaintenanceActions.repair):
           
            self.__calculateCondition(condition,30,15)
            print("Repair Performed")
       
        elif(policy == MaintenanceActions.overhaul):
            self.__calculateCondition(condition,100,5)
            print("Overhaul Performed")
            
            
'''