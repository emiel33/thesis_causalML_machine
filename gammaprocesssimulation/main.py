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


# mean and standard deviations of exogenous variables, [[mean],[stddev]]
# temperatuur - intensityofuse - humidity
mean = [10,9,20]
stddev = [5,3,5]
covariateGenerationArguments = [[mean],[stddev]]

# # # arguments for the gamma process, timeframe, steps(gamma jumps!) , decision points and lamda which remains 1 (?)
# onbelangrijk - aantal increments (steps) - treament decision per hoeveel steps - onbelangrijk
timeframe = 10      # ongebruikt?
timesteps = 50
decisionpoints = 1  # ongebruikt?
lambda_ = 5         # ongebruikt?
processArguments = [timeframe, timesteps, decisionpoints, lambda_]


# Deterioration parameters for the machines under study respectively the
# starting condition, breakdown condition, betas, sigma, maxproduction volume/day
starting_condition = 0      # start with 0 deteriation
breakdown_condition = 1000  # machine breaks down at 1000 deteriation
betas = [math.log(1,e)*25,math.log(1,e)*1,math.log(1,e)*10]  # (?)
sigma = 10 # stddev
maxproduction = 10000 # maxproduction/day
machineParameters = [starting_condition, breakdown_condition, betas, sigma, maxproduction]

machineParametersLabels = ["caseNumber","startingCondition", "breakdownCondition","betas", "sigma", "maxProductionSpeed"]
# define the data labels(columns) of the dataframe
dataLabels = ["caseNumber","steps","temperature","intensityOfUse","humidity","degradationState","degradationAfterTreatment","productionVolume","treatment"]

# define sample parameters
sampleSize = 50 # 50 machines maar? 12000? 10000 training, 1000 val, 1000 test?
trainTestSplit = 1/2

###########################################################################################################################################

def generateSample(samplesize,rng,maintenance,usedMachine = None):
    # pick seed for random generation for repeatability and to determine treatment effect
    
  dataList = list() # list of deteriation?
  machineParametersList = list() # ?
  # if a machine is given, create the process based on the same machine otherwise generate differing machines for each run
  # why?
  if(usedMachine == None):
    for sampleMachine in range(samplesize): # do this 50 times
        machine = Machine(rng)
        process = Deteriorationprocess(processArguments,machine,covariateGenerator,maintenance,rng)
        dataList.extend(process.generaterun())
        machineParametersList.append(machine.getParameters())
  else:
    for sampleMachine in range(samplesize):
        process  = Deteriorationprocess(processArguments,usedMachine,covariateGenerator,maintenance,rng)
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

def formatData(deteriorationData,machineParameterData):
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
  
  # split into test and train dataset
  deteriorationTrainData = deteriorationData.loc[1: round(sampleSize*trainTestSplit)]
  deteriorationTestData = deteriorationData.loc[round(sampleSize*trainTestSplit): sampleSize]

  print(deteriorationData.head(50))

  #output the data to a csv
  deteriorationData.to_csv(os.getcwd() + "/gammaprocesssimulation/deteriorationData.csv")
  deteriorationTrainData.to_csv(os.getcwd() + "/gammaprocesssimulation/deteriorationTrainData.csv")
  deteriorationTestData.to_csv(os.getcwd() + "/gammaprocesssimulation/deteriorationTestData.csv")
  machineParameterData.to_csv(os.getcwd() + "/gammaprocesssimulation/machineParameterData.csv")

  return deteriorationData,machineParameterData


#############################################################################################################################################




rng = np.random.default_rng(10) # use the same seed for generating random numbers

# initialize the exogenous covariate generator / 
# these are not influenced by the current state of the machine but arrise from the use pattern or environment the machine operates in!
covariateGenerator = CovariateGenerator(processArguments,covariateGenerationArguments,rng)

# define machine to use only in case of fixed machine and don't forget to set the parameters to your liking

fixedMachine = Machine(rng) # maak 1 machine, moet altijd dezelfde zijn, aldus emiel
fixedMachine.setParameters(machineParameters)

# define maintenanceProgram for machines/ runs with custom maintenance program if provided in a list!
# define maintanence politiek (random momenteel?)
# here we defne a dependency between maintanence and covariates
dynamicMaintenance = MaintenanceProgram(covariateGenerationArguments,rng)

# generate the sample

deteriorationData,machineParameterData = generateSample(sampleSize,rng,dynamicMaintenance,fixedMachine)
# format data into csv format
deteriorationDatadf,machineParameterDatadf = formatData(deteriorationData,machineParameterData)

# merge the actual outcomeData with the potential outcomeData



# graph data! 
graphSampleData(deteriorationDatadf,"degradationState",processArguments)
graphSampleData(deteriorationDatadf,"cumulativeProduction",processArguments)
graphSampleData(deteriorationDatadf,"productionVolume",processArguments)






# %%
