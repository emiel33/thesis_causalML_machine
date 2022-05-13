
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression

from operator import index
import pandas as pd
import os as os
import numpy as np

# define obervation period of the machine
predictionWindow = 5
start_t = 10

# define sample parameters
sampleSize = 50
trainTestSplit = 1/2

# load dataset 
dataSet = pd.read_csv(os.getcwd() + "/gammaprocesssimulation/deteriorationData.csv", index_col=['caseNumber','steps'])
trainData = dataSet.loc[1: round(sampleSize*trainTestSplit)]
testData =  dataSet.loc[round(sampleSize*trainTestSplit)+1: sampleSize]
#create indexer for multi-index in pandas
idx = pd.IndexSlice

# retrieve the data before timestep t! i.e. the data used for training for the neural network
preTDataSet = trainData.loc[idx[0:,1:start_t-1], : ]

# retrieve data at time step t!
Tanalysis = trainData.loc[(slice(0,None),start_t),]
    # get the treatment at time t from Tanalysis
TTreatment = Tanalysis["treatment"]

# create pivoted table for easier time extraction
pivotedData = trainData.reset_index(level =[0,1] )
pivotedData = pivotedData.pivot(index="caseNumber", columns="steps", values = trainData.columns)

# retrieve the sum of treatments up to but not including timestep t for logistic fit    
logisticFitTreatment = trainData.groupby(["caseNumber"],group_keys = False).apply(lambda x: x[:start_t-1])["treatment"].groupby(["caseNumber"]).sum()

# retrieve covariate for logistic fit
logisticFitCovariates = pivotedData.groupby(["caseNumber"],group_keys=False).apply(lambda x : x.loc[:,(slice(None),slice(start_t-2,start_t-1))]).loc[ :, ( ["temperature","intensityOfUse","humidity"] , slice(None))]


# convert the data to the right format :  (1,t-1) - array (first index =  attributes, second = samplevalues)
logisticFitTreatment = logisticFitTreatment.to_numpy().reshape(-1,1)
logisticFitCovariates = logisticFitCovariates.to_numpy()
    # combine datasets for denomenator model
fullData = np.concatenate((logisticFitCovariates, logisticFitTreatment ), axis = 1)
    #Treatment to array
TTreatment = TTreatment.to_numpy()

# create and fit logistic regressions on history
logregrnumerator = LogisticRegression(penalty= 'l2')
logregrDenomenator = LogisticRegression(penalty= 'l2')
logregrnumerator.fit(logisticFitTreatment, TTreatment)
logregrDenomenator.fit(fullData,TTreatment)

# estimate weights using the logistic regression models! 

currentWeight = 1

for step in range(predictionWindow):
    
    covariateData = pivotedData.groupby(["caseNumber"],group_keys=False).apply(lambda x : x.loc[:,(slice(None),slice(start_t + step - 2,start_t + step-1))]).loc[ :, ( ["temperature","intensityOfUse","humidity"] , slice(None))]
    covariateData = covariateData.to_numpy()

    treatmentData = trainData.groupby(["caseNumber"],group_keys = False).apply(lambda x: x[:start_t + step - 1])["treatment"].groupby(["caseNumber"]).sum()
    treatmentData = treatmentData.to_numpy().reshape(-1,1)

    fullData = np.concatenate((logisticFitCovariates, logisticFitTreatment ), axis = 1)

    numerator = logregrnumerator.predict_proba(treatmentData)[:,0]
    denominator = logregrDenomenator.predict_proba(fullData)[:,0]
    
    element = np.divide(numerator,denominator)
    currentWeight = np.multiply(element,currentWeight)

# retrieve the + 5 cummulative production

cumulativeProducuction = pivotedData.groupby(["caseNumber"],group_keys=False).apply(lambda x : x.loc[:,("cumulativeProduction",start_t + 5)])

covariateData = pivotedData.groupby(["caseNumber"],group_keys=False).apply(lambda x : x.loc[:,(slice(None),slice(start_t + 5 - 2,start_t + 5-1))]).loc[ :, ( ["temperature","intensityOfUse","humidity"] , slice(None))]
covariateData = covariateData.to_numpy()

treatmentData = trainData.groupby(["caseNumber"],group_keys = False).apply(lambda x: x[:start_t + 5 - 1])["treatment"].groupby(["caseNumber"]).sum()
treatmentData = treatmentData.to_numpy().reshape(-1,1)

fullData = np.concatenate((logisticFitCovariates, logisticFitTreatment ), axis = 1)

MSMregression = LinearRegression()
MSMregression.fit(fullData,cumulativeProducuction,currentWeight)

normalRegression = LinearRegression()
normalRegression.fit(fullData,cumulativeProducuction)



# test data prep idem

cumulativeProducuction = pivotedData.groupby(["caseNumber"],group_keys=False).apply(lambda x : x.loc[:,("cumulativeProduction",start_t + 5)])

pivotedData = trainData.reset_index(level =[0,1] )
pivotedData = pivotedData.pivot(index="caseNumber", columns="steps", values = trainData.columns)

covariateData = pivotedData.groupby(["caseNumber"],group_keys=False).apply(lambda x : x.loc[:,(slice(None),slice(start_t + 5 - 2,start_t + 5-1))]).loc[ :, ( ["temperature","intensityOfUse","humidity"] , slice(None))]
covariateData = covariateData.to_numpy()

treatmentData = trainData.groupby(["caseNumber"],group_keys = False).apply(lambda x: x[:start_t + 5 - 1])["treatment"].groupby(["caseNumber"]).sum()
treatmentData = treatmentData.to_numpy().reshape(-1,1)

fullData = np.concatenate((logisticFitCovariates, logisticFitTreatment ), axis = 1)

print("MSMregression:")
print(MSMregression.score(fullData,cumulativeProducuction))
print("normalregression:")
print(normalRegression.score(fullData,cumulativeProducuction))

