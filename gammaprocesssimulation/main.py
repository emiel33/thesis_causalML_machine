#%%

import math
import statistics as stat


import os
import pandas as pd
import matplotlib.pyplot as plt
from gammaProcess import *
from  covariateSeries import *
from maintenance import *
from machine import *
from matplotlib import *


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
###########################################################################################################################################

def generateSample(samplesize,rng,maintenance,covariateGenerator,usedMachine = None):
    # pick seed for random generation for repeatability and to determine treatment effect
    
  dataList = list()
  machineParametersList = list()
  # if a machine is given, create the process based on the same machine otherwise generate differing machines for each run
  if(usedMachine == None):
    for sampleMachine in range(samplesize):
        machine = Machine(rng)
        process  = Deteriorationprocess(processArguments,machine,covariateGenerator,maintenance,rng, sampleMachine)
        dataList.extend(process.generaterun())
        machineParametersList.append(machine.getParameters())
  else:
    for sampleMachine in range(samplesize):
        process  = Deteriorationprocess(processArguments,usedMachine,covariateGenerator,maintenance,rng,sampleMachine)
        dataList.extend(process.generaterun())
        machineParametersList.append(usedMachine.getParameters())
      
  return dataList,machineParametersList

      
# you can select the column in the dataset to display over time example: Cumulative production/ degradationState
def graphSampleData(dataFrame,column,processArguments):
    # format data for plotting
    horizontalTimeSeperation = np.linspace(0,processArguments[1],processArguments[1])
    
    dataFrame = dataFrame.groupby("steps")[column].apply(list)
    
    dataFrame = dataFrame.to_list()
    fig,ax = plt.subplots()
    ax.plot(horizontalTimeSeperation,dataFrame)

    ax.set_title(column + " over time")
    ax.set_ylabel(column)
    ax.set_xlabel("time")

    fig.savefig(column + ".png")

def formatData(deteriorationData,machineParameterData,nameOfCSV):
  # put all the machineparameters into dataframe
  machineParameterData = pd.DataFrame(machineParameterData,columns = machineParametersLabels)
  machineParameterData = machineParameterData.set_index("caseNumber")

  print(deteriorationData)
  # put all deteriorationData and covariates into dataframe
  deteriorationData = pd.DataFrame(deteriorationData, columns = dataLabels)

  print(deteriorationData.head(50))
  #index the data using case and step
  index = pd.MultiIndex.from_frame(deteriorationData.iloc[:,0:2])
  deteriorationData = deteriorationData.drop(["caseNumber","steps"],axis = 1)
  deteriorationData = deteriorationData.set_index(index)

  # add the cummulative production upto that time point for the given case
  deteriorationData["cumulativeProduction"]=deteriorationData.groupby(['caseNumber'])['productionVolume'].cumsum(axis=0)
  

  print(deteriorationData.head(50))

  #output the data to a csv
  deteriorationData.to_csv(nameOfCSV + ".csv")
  machineParameterData.to_csv("machineParameterData" + ".csv")

  return deteriorationData,machineParameterData

def generatePotentialOutcomes(potentialOutcomeTreatments, sampleSize, rng, covariateGenerator,usedMachine = "None"):
  
  # read the treatment actions and calculate the potentialOutcomes dataSet given 
  covariateGenerator = CovariateGenerator(processArguments,covariateGenerationArguments,np.random.default_rng(10))
  dataSet = pd.read_csv(potentialOutcomeTreatments +".csv", index_col=['id'])
  dataSet = dataSet.filter(["step1","step2","step3","step4","step5"])
  dataList = list()
  machineParametersList = list()
  for index,row in dataSet.iterrows():
    row = dataSet.loc[index]
    treatmentPlan = row.to_numpy()
  
    maintenanceProgram = MaintenanceProgram(processArguments,covariateGenerationArguments,np.random.default_rng(10),treatmentplan = treatmentPlan)

    process  = Deteriorationprocess(processArguments,usedMachine,covariateGenerator,maintenanceProgram,rng,index)
    dataList.extend(process.generaterun())
    machineParametersList.append(usedMachine.getParameters())

    return dataList, machineParametersList

  





#############################################################################################################################################
# initialize the exogenous covariate generator / 
# these are not influenced by the current state of the machine but arrise from the use pattern or environment the machine operates in!

# 3 sequences of exogenous covariates inable to recreate similar conditions for potential outcomes!
trainCovariateGenerator= CovariateGenerator(processArguments,covariateGenerationArguments,np.random.default_rng(2))
testcovariateGenerator = CovariateGenerator(processArguments,covariateGenerationArguments,np.random.default_rng(2))
testPotentialOutcomeGenerator = CovariateGenerator(processArguments,covariateGenerationArguments,np.random.default_rng(2))

# define machine to use only in case of fixed machine and don't forget to set the parameters to your liking!

fixedMachine = Machine(np.random.default_rng(10))
fixedMachine.setParameters(machineParameters)

# create dynamic maintenancePlan

dynamicMaintenance = MaintenanceProgram(processArguments,covariateGenerationArguments,np.random.default_rng(10), treatmentplan ="policy")
# create sample for 
rng = np.random.default_rng(1)

POpolicyData,POmachineParameterData = generateSample(PotentialOutcomeSize, rng, dynamicMaintenance ,testPotentialOutcomeGenerator,usedMachine = fixedMachine)
testData,testMachineParameterData = generateSample(testSize,rng,dynamicMaintenance,testcovariateGenerator,usedMachine = fixedMachine)
trainData,trainMachineParameterData = generateSample(trainingSize,rng,dynamicMaintenance,trainCovariateGenerator,usedMachine = fixedMachine)


POpolicyDatadf,POmachineParameterDatadf = formatData(POpolicyData,POmachineParameterData,"POpolicyData")
testDatadf,testMachineParameterDatadf = formatData(testData,testMachineParameterData ,"testData")
trainDatadf,trainMachineParameterDatadf = formatData(trainData,trainMachineParameterData,"trainData")

rng = np.random.default_rng(1)

POcustomData,POmachineParameterData = generatePotentialOutcomes("potentialOutcomeTreatments",PotentialOutcomeSize, rng, testPotentialOutcomeGenerator,usedMachine = fixedMachine)


POcustomDatadf,POmachineParameterDatadf = formatData(POcustomData,POmachineParameterData,"POcustomData")




'''


# define maintenanceProgram for machines/ runs with custom maintenance program if provided in a list to setTreatmentPlan or random after given start prediciton parameter!

dynamicMaintenance = MaintenanceProgram(processArguments,covariateGenerationArguments,np.random.default_rng(10), treatmentplan ="policy")

# From the startpoint till the end this maintenance scheme is used: Must provide list with treatments of length steps - starttime + 1 
Fmaintenance = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
fixedMaintenance = MaintenanceProgram(processArguments,covariateGenerationArguments,np.random.default_rng(10),treatmentplan = Fmaintenance)

#random treatment plan

randomMaintenance = MaintenanceProgram(processArguments,covariateGenerationArguments,np.random.default_rng(10),treatmentplan = "random")


# generate the sample
deteriorationDataDyn,machineParameterDataDyn = generateSample(sampleSize,np.random.default_rng(0),dynamicMaintenance,covariateGenerator,fixedMachine)
deteriorationDataFi,machineParameterDataFi = generateSample(sampleSize,np.random.default_rng(0),fixedMaintenance,covariateGenerator2,fixedMachine)
deteriorationDataRand,machineParameterDataRand = generateSample(sampleSize,np.random.default_rng(0),randomMaintenance,covariateGenerator3,fixedMachine)

# format data into csv format
deteriorationDataDyndf,machineParameterDataDyndf = formatData(deteriorationDataDyn,machineParameterDataDyn,"PolicydeteriorationData")
deteriorationDataFidf,machineParameterDataFidf = formatData(deteriorationDataFi,machineParameterDataFi,"FixedPlanDeteriorationData")
deteriorationDataRanddf,machineParameterDataRanddf = formatData(deteriorationDataRand,machineParameterDataRand,"randomDeterionData")
# merge the actual outcomeData with the potential outcomeData



# graph data! 
graphSampleData(deteriorationDataDyndf,"degradationState",processArguments)
graphSampleData(deteriorationDataDyndf,"cumulativeProduction",processArguments)
graphSampleData(deteriorationDataDyndf,"productionVolume",processArguments)



'''


# %%
