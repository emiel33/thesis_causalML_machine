import numpy as np
import pandas as pd
import os as os

# load data in dataframe with correct indices
dataset = pd.read_csv(os.getcwd() + "/dataset.csv",",",index_col= ["case","step"])

# display dataframe
print(dataset)


# calculate the gamma jumps between the timestep! Check if this comes out correct!
condition = dataset.get("condition")

difference = condition.groupby("case").diff(periods = 1)


# reformulate data into timestep columns
#add the condition of the final timestep for analysis

reformated = dataset.reset_index(1)
averageTreatmentResponse = reformated.groupby("case")["treatment"].apply(list)
treatmentHistory = averageTreatmentResponse.tolist()
treatmentHistory = pd.DataFrame(treatmentHistory)
print(treatmentHistory)

treatmentHistory.columns = ["TimePoint "+ str(i) for i in treatmentHistory.columns]

#treatment.rename({0:"period 0",1:"period 1",2:"period 2",3: "period 3", 4:"period 4", 5:"period 5",6:"period 6",7:"period 7"},axis = 1,inplace=True)
endCondition = reformated.loc[reformated["step"]==5].loc[:,"condition"]
treatmentHistory["condition"] = endCondition
print(treatmentHistory)
columns = treatmentHistory.columns.tolist()
columns.remove("condition")

treatmentHistory = treatmentHistory.groupby(columns).agg("mean")
print(treatmentHistory)
treatmentHistory[treatmentHistory["period 1"] ==1]
#naiveAverageTreatmentEffect = treatment[treatment.columns ==[1,1,1,1,1,1,1,1,1,1]]



#print(averageTreatmentResponse)
#averageTreatmentResponse["condition"]=dataset.loc[dataset["condition"] == 5].get("condition")


#averageTreatmentResponse = averageTreatmentResponse.groupby("step").aggregate(np.average)
#print(averageTreatmentResponse.iloc[:,0].unique())



