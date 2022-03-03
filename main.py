#%%


import os
import pandas as pd
import matplotlib.pyplot as plt
from gammaProcess import *
from  exogenous import *
from maintenance import *
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
generationArguments = [[10,5,20],[2,1,3]]
# arguments for the gamma process, timeframe and steps(gamma jumps!)
processArguments = [10,6]
steps = processArguments[1]
# Deterioration parameters for the machines under study respectively the
# starting condition, breakdown condition, betas, sigma and scale parameter
machineParameters = [0,100000000,[0.3/10,0.6/5,0.5/20],5,1]
# define the data labels for dataframe
dataLabels = ["case","steps","temperature","intensityOfUse","environment","condition","treatment"]
# define sample parameters
samplesize = 10

# initialize the exogenous covariate generator / 
# these are not influenced by the current state of the machine
covGen = CovariateGenerator(processArguments,generationArguments)
covariates  = covGen.generateCovariateTimeSeries()


# initialize machine under study with it's parameters
exampleMachine = Machine(machineParameters)

#initialize treatment policy depending on normal conditions ("apparant" state of the machine has not been taken into account yet)
maintenance = MaintenanceAction(generationArguments[0],generationArguments[1])

#intialize deteriorationprocess using gamma jumps
# using machine, process arguments, covariates and the maintenance policy
detProc = Deteriorationprocess(processArguments,exampleMachine,covariates,maintenance)

# generate one deterioration process, returns the condition and treatment decisions made


data = list()
for sample in range(samplesize):
    
    for step in range(steps):
        
        run = list()

        process = detProc.generaterun()
        condition = process[0]
        treatment = process[1]
        
        run.append(sample)
        run.append(step)
        run.extend(covariates[step])
        run.append(condition[step])
        run.append(treatment[step])
        print(run)
        data.append(run)


data = pd.DataFrame(data, columns = dataLabels)
print(data)
index = pd.MultiIndex.from_frame(data.iloc[:,0:2])
data = data.drop(["case","steps"],axis = 1)
print(data)
data = data.set_index(index)

data.to_csv(os.getcwd() + "/dataset.csv",",",index_label = "index")

print(data)




'''
def generatesample(samplesize,processArgs, covariates):
    run = []
    
    steps= processArgs[0]
    scaleparameter = processArgs[1]


    for i in range(samplesize) :
        newrun = generaterun(steps,scaleparameter,covariates)
        run.append(newrun)
   
    return run      

'''










'''
dataSet = pd.DataFrame(attributes, columns= dataLabels)
dataSet = dataSet.set_index(["caseId","timeIndex"])
print(dataSet.head(20))
'''
'''



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
        







# %%
