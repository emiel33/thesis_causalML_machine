from matplotlib import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os




# you can select the column in the dataset to display over time example: Cumulative production/ degradationState
def graphSampleData(dataFrame,column,steps):
    # format data for plotting
    horizontalTimeSeperation = np.linspace(0,steps,steps)
    
    dataFrame = dataFrame.groupby("steps")[column].apply(list)
    
    dataFrame = dataFrame.to_list()
    fig,ax = plt.subplots()
    ax.plot(horizontalTimeSeperation,dataFrame, color = 'r')

    ax.set_title(column + " over time")
    ax.set_ylabel(column)
    ax.set_xlabel("time")

    fig.savefig(column + ".png")

def graphComparisonData(dataFrame1,dataFrame2,column,steps):
    # format data for plotting
    horizontalTimeSeperation = np.linspace(0,steps,steps)
    
    dataFrame1 = dataFrame1.groupby("steps")[column].apply(list)
    dataFrame2 = dataFrame2.groupby("steps")[column].apply(list)
    
    dataFrame1 = dataFrame1.to_list()
    dataFrame2= dataFrame2.to_list()
   
    fig,ax = plt.subplots()
    
    ax.plot(horizontalTimeSeperation,dataFrame1,color = 'r')
    ax.plot(horizontalTimeSeperation,dataFrame2,color = 'b')

    ax.set_title(column + " over time")
    ax.set_ylabel(column)
    ax.set_xlabel("time")

    fig.savefig(os.getcwd  + column + ".png")




POpolicyDatadf= pd.read_csv("POpolicyData.csv", index_col=['caseNumber','steps'])
subindex = POpolicyDatadf.index.get_level_values('caseNumber')
sample_caseNumbers = np.random.choice(subindex, 5, replace=False)
POpolicyDatadf= POpolicyDatadf.loc[(sample_caseNumbers,slice(40,50)),]

graphSampleData(POpolicyDatadf,"cumulativeProduction",10)
graphSampleData(POpolicyDatadf,"degradationState",10)

POcustomDatadf = pd.read_csv("POcustomData.csv", index_col=['caseNumber','steps'])


