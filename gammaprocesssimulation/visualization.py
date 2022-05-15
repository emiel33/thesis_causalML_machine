from matplotlib import *
from matplotlib import figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

import math

print(math.log(1,math.e)*25)

# you can select the column in the dataset to display over time example: Cumulative production/ degradationState
def graphSampleData(dataFrame,column,steps):
    # format data for plotting
    horizontalTimeSeperation = np.linspace(0,steps,steps)
    
    dataFrame = dataFrame.groupby("steps")[column].apply(list)
    
    dataFrame = dataFrame.to_list()
    fig,ax= plt.subplots()

   
    ax.plot(horizontalTimeSeperation,dataFrame)

    ax.set_title(column + " over time")
    ax.set_ylabel(column)
    ax.set_xlabel("step")

    fig.savefig(column + ".png")

def graphComparisonData(dataFrame1,dataFrame2,column,steps):
    # format data for plotting
    horizontalTimeSeperation = np.linspace(0,steps,steps)
    
    dataFrame1 = dataFrame1.groupby("steps")[column].apply(list)
    dataFrame2 = dataFrame2.groupby("steps")[column].apply(list)
    
    dataFrame1 = dataFrame1.to_list()
    dataFrame2= dataFrame2.to_list()
   
    fig,ax = plt.subplots()
    
    ax.axes([None,None,0,None])
    
    ax.set_ylim([0,None])
    ax.set_title(column + " over time")
    ax.set_ylabel(column)
    ax.set_xlabel("step")

    ax.plot(horizontalTimeSeperation,dataFrame1)
    ax.plot(horizontalTimeSeperation,dataFrame2)
    
    

    fig.savefig(os.getcwd  + column + ".png")


rng =np.random.default_rng(5)

POpolicyDatadf= pd.read_csv("POpolicyData.csv", index_col=['caseNumber','steps'])
subindex = POpolicyDatadf.index.get_level_values('caseNumber')
sample_caseNumbers = rng.choice(subindex, 2, replace=False)
POpolicyDatadf= POpolicyDatadf.loc[(sample_caseNumbers,slice(0,50)),]

graphSampleData(POpolicyDatadf,"productionVolume",50)
graphSampleData(POpolicyDatadf,"degradationState",50)

POcustomDatadf = pd.read_csv("POcustomData.csv", index_col=['caseNumber','steps'])


