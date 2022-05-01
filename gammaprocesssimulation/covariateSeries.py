#%%
import numpy as np
from scipy.stats import random_correlation


#generate covariance matrix to indicate relationship between covariates appearing 

class CovariateGenerator:

    def __init__(self,processArguments,generationArguments,rng):
       
        # general process parameters
        self.timeFrame = processArguments[0] #ongebruikt ?
        self.steps = processArguments[1]
        self.stepsize = self.timeFrame/self.steps # ongebruikt ?

        # parameters for exogenous variable generation
        self.mean = generationArguments[0]
        self.standarddev = generationArguments[1]
        self.rng = rng
        self.covariance = self.__generateCovarianceMatrix(self.rng)


    def __generateCovarianceMatrix(self,rng):

        # Corrolationmatrix C from eigenvector
        # diagonaalmatrix met stddev D
        # covariance = C*D*C

        # generate random correlation matrix 
        # each eigenvalue represents percentage explained covariance of dimension/4 (?)
        # parameters must always sum to dimension of correlation matrix ( thus total explained covariance = 1) (?)
        # eigenvector =
        eig = (.5, .9, 1.6) # zelf verzonnen? why?
        C = random_correlation.rvs(eig, random_state=rng) # random getallen behalve op diagonaal -> 1, symmetrisch
        # create diagonally filled matrix with standarddevs
        D = np.diag(self.standarddev) # overal 0 behalve op diagonaal -> stddev
        # create covariance matrix based on the standdardevs and random correlation matrix
        # covariance = np.matmul(standarddevMatrix,np.matmul(correlationMatrix,standarddevMatrix)) # i (evelien) would do it like this:
        covariance = C.dot(D).dot(C)
        return covariance
    
    def generateCovariateTimePoint(self): # why?
        
        # should we add bias here?
        covariates = list(self.rng.multivariate_normal(self.mean, self.covariance))
        return covariates

    def generateCovariateTimeSeries(self):
        covariateTimeSeries = list()
        
        for step in range(self.steps):
            covariates = self.generateCovariateTimePoint()
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