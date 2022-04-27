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

# arguments for the gamma process, timeframe, steps(gamma jumps!) , decision points and lamda which remains 1
processArguments = [10,50,1,5]
steps = processArguments[1]


# Deterioration parameters for the machines under study respectively the
# starting condition, breakdown condition, betas, sigma, maxproduction volume/day
machineParameters = [0,1000,[math.log(1,e)/10,math.log(1,e)/9,math.log(1,e)/20],0.01,10000]



machineParametersLabels = ["caseNumber","startingCondition", "breakdownCondition","betas", "sigma", "maxProductionSpeed"]
# define the data labels(columns) of the dataframe
dataLabels = ["caseNumber","steps","temperature","intensityOfUse","humidity","degradationState","degradationAfterTreatment","productionVolume","treatment"]

# define sample parameters
samplesize = 2

###########################################################################################################################################

def generateSample(samplesize,rng,maintenance,usedMachine = None):
    # pick seed for random generation for repeatability and to determine treatment effect
    
  dataList = list()
  machineParametersList = list()
  # if a machine is given, create the process based on the same machine otherwise generate differing machines for each run
  if(usedMachine == None):
    for sampleMachine in range(samplesize):
        machine = Machine(rng)
        process  = Deteriorationprocess(processArguments,machine,covariateGenerator,maintenance,rng)
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

  #output the data to a csv
  deteriorationData.to_csv(os.getcwd() + "/gammaprocesssimulation/deteriorationData.csv")
  machineParameterData.to_csv(os.getcwd() + "/gammaprocesssimulation/machineParameterData.csv")

  return deteriorationData,machineParameterData


#############################################################################################################################################




rng = np.random.default_rng(10)

# initialize the exogenous covariate generator / 
# these are not influenced by the current state of the machine but arrise from the use pattern or environment the machine operates in!
covariateGenerator = CovariateGenerator(processArguments,covariateGenerationArguments,rng)

# define machine to use only in case of fixed machine and don't forget to set the parameters to your liking

fixedMachine = Machine(rng)
fixedMachine.setParameters(machineParameters)

# define maintenanceProgram for machines/ runs with custom maintenance program if provided in a list!

dynamicMaintenance = MaintenanceProgram(covariateGenerationArguments,rng)

# generate the sample

deteriorationData,machineParameterData = generateSample(samplesize,rng,dynamicMaintenance,fixedMachine)
# format data into csv format
deteriorationDatadf,machineParameterDatadf = formatData(deteriorationData,machineParameterData)

# merge the actual outcomeData with the potential outcomeData



# graph data! 
graphSampleData(deteriorationDatadf,"degradationState",processArguments)
graphSampleData(deteriorationDatadf,"cumulativeProduction",processArguments)
graphSampleData(deteriorationDatadf,"productionVolume",processArguments)






# %%
