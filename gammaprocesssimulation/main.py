#%%


import os
import pandas as pd
import matplotlib.pyplot as plt
from gammaProcess import *
from  covariateSeries import *
from maintenance import *
from machine import *
import matplotlib.pyplot  as mp



"""

timestep = 1

# mean jump size parameter of the gammaprocess
mean_parameter = 0.25
#mean variance of jump sizeparameter of the gammaprocess
variance_parameter = 0.25

# conversion to normal gamma parameters
shapeParameter = (mean_parameter**2/stepsize)/variance_parameter
scaleParameter = variance_parameter/mean_parameter

#alpha(t)/ beta = mean jump
#
"""
#TO DO: resolve positive definiteness,  importance: low
#       add dependencies over time,     imortance: high
#       add endogenous dependencies,    importance: high
#       treatments should not happen to often! there should be more of them


# mean and standard deviations of exogenous variables,mean and stddev
covariateGenerationArguments = [[10,5,20],[2,1,3]]

# arguments for the gamma process, timeframe, steps(gamma jumps!) and lamda which remains 1
processArguments = [2,10,1]
steps = processArguments[1]


# Deterioration parameters for the machines under study respectively the
# starting condition, breakdown condition, betas, sigma, maxproduction volume/day
machineParameters = [0,1000,[0.3/10,0.6/5,0.5/20],5,100]

# define the data labels(columns) of the dataframe
dataLabels = ["case","steps","temperature","intensityOfUse","environment","condition","sensorData","productionVolume","treatment"]

# define sample parameters
samplesize = 200

###########################################################################################################################################

# initialize the exogenous covariate generator / 
# these are not influenced by the current state of the machine but arrise from the use pattern or environment the machine operates in!
covariateGenerator = CovariateGenerator(processArguments,covariateGenerationArguments)
# initialize machine under study with it's parameters
exampleMachine = Machine(machineParameters)
# define maintenanceProgram for machine
maintenance = MaintenanceProgram(covariateGenerationArguments,exampleMachine)
#intialize deteriorationprocess using gamma jumps
# using machine, process arguments, covariates and the maintenance policy
detProc = Deteriorationprocess(processArguments,exampleMachine,covariateGenerator,maintenance)

# generate sample of processes
dataList = list()
for case in range(samplesize):
    for step in range(steps):
        
        run = detProc.generaterun()[step]
        run.insert(0,case)
        dataList.append(run)
    
# put all data in a dataframe
data = pd.DataFrame(dataList, columns = dataLabels)

#index the data using case and step
index = pd.MultiIndex.from_frame(data.iloc[:,0:2])
data = data.drop(["case","steps"],axis = 1)
data = data.set_index(index)
data.round(1)
# add the cummulative production upto that time point for the given case
data["cumumulativeProduction"]=data.groupby(['case'])['productionVolume'].cumsum(axis=0)

#output the data to a csv
data.to_csv(os.getcwd() + "\gammaprocesssimulation\dataset.csv",",",index_label = ["case","step"])
print(data.head(30))



"""



#write dataset to csv file in provided relative path from the currrent working directory

covariates= dataSet[['temperature','intensityOfUse','environment']]
covariates = covariates.to_dict

print(covariates)

# generate gamma process sample given data
sample = generatesample(10,processArgs,covariates)

condition = list(sample[0].values())
time = list(sample[0].keys())
condition2 = list(sample[1].values())
time2 = list(sample[1].keys())
condition3 = list(sample[2].values())
time3 = list(sample[2].keys())
condition4 = list(sample[3].values())
time4 = list(sample[3].keys())


plt.scatter(time,condition)
plt.scatter(time2,condition2)
plt.scatter(time3,condition3)
plt.scatter(time4,condition4)
plt.show()

'''
        



"""



# %%
