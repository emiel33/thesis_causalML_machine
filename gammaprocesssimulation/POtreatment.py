import os
import pandas as pd
import matplotlib.pyplot as plt
from gammaProcess import *
from  covariateSeries import *
from maintenance import *
from machine import *
from matplotlib import *
import math

# mean and standard deviations of exogenous variables,mean and stddev
covariateGenerationArguments = [[10,9,20],[5,3,5]]

# arguments for the gamma process, timeframe, steps(gamma jumps!) , decision points and lamda which remains 1,start time t (from this time the machinelearning algorithm starts predicting outcomes)
processArguments = [10,50,1,5,20,24]
steps = processArguments[1]


# Deterioration parameters for the machines under study respectively the
# starting condition, breakdown condition, betas, sigma, maxproduction volume/day
machineParameters = [0,10000,[math.log(1,e)*25,math.log(1,e)*1,math.log(1,e)*10],5,10000]



machineParametersLabels = ["caseNumber","startingCondition", "breakdownCondition","betas", "sigma", "maxProductionSpeed"]
# define the data labels(columns) of the dataframe
dataLabels = ["caseNumber","steps","temperature","intensityOfUse","humidity","degradationState","degradationAfterTreatment","productionVolume","treatment"]

# define trainingset
trainingSize = 5000

#define test set
testSize = 1000

# define set for potentialOuctomes

PotentialOutcomeSize = 100



def generatePotentialOutcomes(potentialOutcomeTreatments, sampleSize, rng, covariateGenerator,usedMachine = "None"):
  
  # read the treatment actions and calculate the potentialOutcomes dataSet given 
  
  dataSet = pd.read_csv(os.getcwd() + "/" +potentialOutcomeTreatments +".csv", index_col=['id'])
  dataSet = dataSet.filter(["step1","step2","step3","step4","step5"])
  dataList = list()
  machineParametersList = list()
  
  for index,rows in dataSet.iterrows():
    row = dataSet.loc[index]
    treatmentPlan = row.to_numpy()
    print(index)
    print("hello")
    print(treatmentPlan)
    
    maintenanceProgram = MaintenanceProgram(processArguments,covariateGenerationArguments,np.random.default_rng(10),treatmentplan = treatmentPlan)

    process  = Deteriorationprocess(processArguments,usedMachine,covariateGenerator,maintenanceProgram,rng,index)
    dataList.extend(process.generaterun())
    machineParametersList.append(usedMachine.getParameters())

  return dataList, machineParametersList


def formatData(deteriorationData,machineParameterData,nameOfCSV):
  # put all the machineparameters into dataframe
  machineParameterData = pd.DataFrame(machineParameterData,columns = machineParametersLabels)
  machineParameterData = machineParameterData.set_index("caseNumber")


  # put all deteriorationData and covariates into dataframe
  deteriorationData = pd.DataFrame(deteriorationData, columns = dataLabels)

 
  #index the data using case and step
  index = pd.MultiIndex.from_frame(deteriorationData.iloc[:,0:2])
  deteriorationData = deteriorationData.drop(["caseNumber","steps"],axis = 1)
  deteriorationData = deteriorationData.set_index(index)

  # add the cummulative production upto that time point for the given case
  deteriorationData["cumulativeProduction"]=deteriorationData.groupby(['caseNumber'])['productionVolume'].cumsum(axis=0)
  



  #output the data to a csv
  deteriorationData.to_csv(nameOfCSV + ".csv")
  machineParameterData.to_csv("machineParameterData" + ".csv")

  return deteriorationData,machineParameterData

# define machine
fixedMachine = Machine(np.random.default_rng(10))
fixedMachine.setParameters(machineParameters)

# define covariate generator
testPotentialOutcomeGenerator2 = CovariateGenerator(processArguments,covariateGenerationArguments,np.random.default_rng(3))

rng = np.random.default_rng(1)

POcustomData,POmachineParameterData = generatePotentialOutcomes("potentialOutcomeTreatments",PotentialOutcomeSize, rng, testPotentialOutcomeGenerator2,usedMachine = fixedMachine)

POcustomDatadf,POmachineParameterDatadf = formatData(POcustomData,POmachineParameterData,"POcustomData")
