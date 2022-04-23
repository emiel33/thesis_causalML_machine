#%%


import os
import pandas as pd
import matplotlib.pyplot as plt
from gammaProcess import *
from  covariateSeries import *
from maintenance import *
from machine import *
import matplotlib.pyplot  as plt

def generateSample(samplesize,rng,rng2):
    # pick seed for random generation for repeatability and to determine treatment effect
    
    dataList = list()
    machineParametersList = list()
    for machine in range(samplesize):
      machine = Machine(rng)
      process  = Deteriorationprocess(processArguments,machine,covariateGenerator,maintenance,rng2)
      dataList.extend(process.generaterun())
      machineParametersList.append(machine.getParameters())
      
    return dataList,machineParametersList

      
# you can select the column in the dataset to display over time example: Cumulative production/ degradationState
def graphSampleData(dataframe,column,processArguments):
    # format data for plotting
    horizontalTimeSeperation = np.linspace(0,processArguments[1],processArguments[1])
    dataframe = dataframe.groupby("steps")[column].apply(list)
    apple = dataframe.to_list()

    plt.plot(horizontalTimeSeperation,apple)
    plt.ylabel(column)
    plt.savefig(column + ".png")  

#############################################################################################################################################

# mean and standard deviations of exogenous variables,mean and stddev
covariateGenerationArguments = [[10,9,20],[5,3,5]]

# arguments for the gamma process, timeframe, steps(gamma jumps!) and lamda which remains 1
processArguments = [10,80,1]
steps = processArguments[1]


# Deterioration parameters for the machines under study respectively the
# starting condition, breakdown condition, betas, sigma, maxproduction volume/day
machineParameters = [0,3000,[0.2/10,0.5/5,0.3/20],2,100]



machineParametersLabels = ["caseNumber","startingCondition", "breakdownCondition","betas", "sigma", "maxProductionSpeed"]
# define the data labels(columns) of the dataframe
dataLabels = ["caseNumber","steps","temperature","intensityOfUse","humidity","degradationState","sensorData","productionVolume","treatment"]

# define sample parameters
samplesize = 20

###########################################################################################################################################


rng = np.random.default_rng(10)
rng2 = np.random.default_rng(5)
# initialize the exogenous covariate generator / 
# these are not influenced by the current state of the machine but arrise from the use pattern or environment the machine operates in!
covariateGenerator = CovariateGenerator(processArguments,covariateGenerationArguments,rng)

# define maintenanceProgram for machines
maintenance = MaintenanceProgram(covariateGenerationArguments,rng)





deteriorationData,machineParameterData = generateSample(samplesize,rng,rng2)

machineParameterData = pd.DataFrame(machineParameterData,columns = machineParametersLabels)
machineParametersData = machineParameterData.set_index("caseNumber",inplace =True)
print(machineParameterData)

# put all data in a dataframe
deteriorationData = pd.DataFrame(deteriorationData, columns = dataLabels)

#index the data using case and step
index = pd.MultiIndex.from_frame(deteriorationData.iloc[:,0:2])
deteriorationData = deteriorationData.drop(["caseNumber","steps"],axis = 1)
deteriorationData = deteriorationData.set_index(index)
deteriorationData.round(1)
# add the cummulative production upto that time point for the given case
deteriorationData["cumulativeProduction"]=deteriorationData.groupby(['caseNumber'])['productionVolume'].cumsum(axis=0)

#output the data to a csv
deteriorationData.to_csv(os.getcwd() + "\gammaprocesssimulation\dataset.csv",",",index_label = ["case","step"])
print(deteriorationData.head(30))

graphSampleData(deteriorationData,"degradationState",processArguments)
graphSampleData(deteriorationData,"cumulativeProduction",processArguments)
graphSampleData(deteriorationData,"productionVolume",processArguments)




# %%
