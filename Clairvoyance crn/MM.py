# Necessary packages
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import warnings
warnings.filterwarnings('ignore')

import sys, os
sys.path.append(os.path.realpath('..'))


#from utils import PipelineComposer

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# write alll print output to program output file
file_path = 'program output.txt'
sys.stdout = open(file_path, "w")

# IN THE NEXT PART LOAD THE DATA SET AND FORMAT IT AS NEEDED

from datasets.data_loader import CSVLoader

# Define data name
data_name = 'machine_6'
# Define data dictionary
data_directory = data_name + '/' + data_name + '_'

# Load train and test datasets
data_loader_training = CSVLoader(static_file=data_directory + 'static_train_data.csv',
                                 temporal_file=data_directory + 'temporal_train_data_eav.csv')

data_loader_testing = CSVLoader(static_file=data_directory + 'static_test_data.csv',
                                temporal_file=data_directory + 'temporal_test_data_eav.csv')

dataset_training = data_loader_training.load()
dataset_testing = data_loader_testing.load()

print('Finish data loading.')






#DEFINE PROBLEM
from preprocessing.encoding import ProblemMaker
# Define parameters
problem = 'online'
max_seq_len = 20
label_name = 'productionVolume' #label name of production capacity, colum that will be tracked
treatment = ['treatment']#label name of the repair/maintenance
window = 1

# Define problem 
problem_maker = ProblemMaker(problem=problem, label=[label_name],
                             max_seq_len=max_seq_len, treatment=treatment, window=window)

dataset_training = problem_maker.fit_transform(dataset_training)
dataset_testing = problem_maker.fit_transform(dataset_testing)

# Set other parameters
metric_name = 'mse' #optimize the Area Under Curve
task = 'classification' # treatment either happens or not so classification

metric_sets = [metric_name]
metric_parameters =  {'problem': problem, 'label_name': [label_name]}

print('Finish defining problem.')


 
 
# LEARN AND PREDICT
from treatments.treatments import treatment_effects_model

# Set the treatment effects model
model_name = 'CRN'
projection_horizon = 5

# Set up validation for early stopping and best model saving
dataset_training.train_val_test_split(prob_val=0.2, prob_test = 0.0)


model_parameters={'encoder_rnn_hidden_units': 128,
                  'encoder_br_size': 64,
                  'encoder_fc_hidden_units': 128,
                  'encoder_learning_rate': 0.001,
                  'encoder_batch_size': 256,
                  'encoder_keep_prob': 0.9,
                  'encoder_num_epochs': 100,
                  'encoder_max_alpha': 1.0,
                  'decoder_br_size': 64,
                  'decoder_fc_hidden_units': 128,
                  'decoder_learning_rate': 0.001,
                  'decoder_batch_size': 512,
                  'decoder_keep_prob': 0.9,
                  'decoder_num_epochs': 100,
                  'decoder_max_alpha': 1.0,
                  'projection_horizon': 5,
                  'static_mode': 'concatenate',
                  'time_mode': 'concatenate'}
treatment_model = treatment_effects_model(model_name, model_parameters, task='classification')
treatment_model.fit(dataset_training)
    

# Return the factual predictions on the testing set
test_y_hat = treatment_model.predict(dataset_testing)

print('Finish treatment effects model training and testing.')

from evaluation import Metrics
from evaluation import print_performance

# Evaluate predictor model
result = Metrics(metric_sets, metric_parameters).evaluate(dataset_testing.label, test_y_hat)
print('Finish predictor model evaluation.')

print('Overall performance')
print_performance(result, metric_sets, metric_parameters)

print("results")
print (result)
print("overall result")
print(np.nanmean(result[' productionvolume + mse']))




  # Predict and visualize counterfactuals for the sequence of treatments indicated by the user through the treatment_options
def all_options():
    return np.array([[[0], [1], [1], [1], [1], [1]],
 [[0], [1], [1], [1], [1], [0]],
 [[0], [1], [1], [1], [0], [1]],
 [[0], [1], [1], [1], [0], [0]],
 [[0], [1], [1], [0], [1], [1]],
 [[0], [1], [1], [0], [1], [0]],
 [[0], [1], [1], [0], [0], [1]],
 [[0], [1], [1], [0], [0], [0]],
 [[0], [1], [0], [1], [1], [1]],
 [[0], [1], [0], [1], [1], [0]],
 [[0], [1], [0], [1], [0], [1]],
 [[0], [1], [0], [1], [0], [0]],
 [[0], [1], [0], [0], [1], [1]],
 [[0], [1], [0], [0], [1], [0]],
 [[0], [1], [0], [0], [0], [1]],
 [[0], [1], [0], [0], [0], [0]],
 [[0], [0], [1], [1], [1], [1]],
 [[0], [0], [1], [1], [1], [0]],
 [[0], [0], [1], [1], [0], [1]],
 [[0], [0], [1], [1], [0], [0]],
 [[0], [0], [1], [0], [1], [1]],
 [[0], [0], [1], [0], [1], [0]],
 [[0], [0], [1], [0], [0], [1]],
 [[0], [0], [1], [0], [0], [0]],
 [[0], [0], [0], [1], [1], [1]],
 [[0], [0], [0], [1], [1], [0]],
 [[0], [0], [0], [1], [0], [1]],
 [[0], [0], [0], [1], [0], [0]],
 [[0], [0], [0], [0], [1], [1]],
 [[0], [0], [0], [0], [1], [0]],
 [[0], [0], [0], [0], [0], [1]],
 [[0], [0], [0], [0], [0], [0]],
 [[1], [1], [1], [1], [1], [1]],
 [[1], [1], [1], [1], [1], [0]],
 [[1], [1], [1], [1], [0], [1]],
 [[1], [1], [1], [1], [0], [0]],
 [[1], [1], [1], [0], [1], [1]],
 [[1], [1], [1], [0], [1], [0]],
 [[1], [1], [1], [0], [0], [1]],
 [[1], [1], [1], [0], [0], [0]],
 [[1], [1], [0], [1], [1], [1]],
 [[1], [1], [0], [1], [1], [0]],
 [[1], [1], [0], [1], [0], [1]],
 [[1], [1], [0], [1], [0], [0]],
 [[1], [1], [0], [0], [1], [1]],
 [[1], [1], [0], [0], [1], [0]],
 [[1], [1], [0], [0], [0], [1]],
 [[1], [1], [0], [0], [0], [0]],
 [[1], [0], [1], [1], [1], [1]],
 [[1], [0], [1], [1], [1], [0]],
 [[1], [0], [1], [1], [0], [1]],
 [[1], [0], [1], [1], [0], [0]],
 [[1], [0], [1], [0], [1], [1]],
 [[1], [0], [1], [0], [1], [0]],
 [[1], [0], [1], [0], [0], [1]],
 [[1], [0], [1], [0], [0], [0]],
 [[1], [0], [0], [1], [1], [1]],
 [[1], [0], [0], [1], [1], [0]],
 [[1], [0], [0], [1], [0], [1]],
 [[1], [0], [0], [1], [0], [0]],
 [[1], [0], [0], [0], [1], [1]],
 [[1], [0], [0], [0], [1], [0]],
 [[1], [0], [0], [0], [0], [1]],
 [[1], [0], [0], [0], [0], [0]]])

def calc_best(patient_history, treatment_options, counterfactual_predictions):
    """Visualize the counterfactual predictions.

    Args:
        - patient_history
        - treatment_options
        - counterfactual_predictions

    Returns:
        - Counterfactual predictions in graph
    """
    prediction_horizon = treatment_options.shape[1]
    history_length = patient_history.shape[0]
    best=0
    best_value=0
    totals=[]
    for (index, counterfactual) in enumerate(counterfactual_predictions):
        #print("counter", index, counterfactual)
        s=0
        for i in counterfactual:
            s+=i
        totals.append(s)
        if s>best_value:
            best_value=s
            best=index
        #print("som",s)
    #print(best,best_value)
    return best
#treatment_options = np.array([[[1], [1], [1], [1], [1], [0]]
#                                 ,[[0], [0], [0], [0], [1], [1]]])
treatment_options=all_options()

history, counterfactual_traj = treatment_model.predict_counterfactual_trajectories(dataset=dataset_testing,
                                                                            patient_id=6, timestep=5,
                                                                            treatment_options=treatment_options)

#from evaluation import print_counterfactual_predictions
#print_counterfactual_predictions(patient_history=history, treatment_options=treatment_options,
#                                   counterfactual_predictions=counterfactual_traj)
#
#desired=calc_best(patient_history=history, treatment_options=treatment_options,
#                                counterfactual_predictions=counterfactual_traj)
#print("treatment paln for ",6,treatment_options[desired])

for i in range(10):

    history, counterfactual_traj = treatment_model.predict_counterfactual_trajectories(dataset=dataset_testing,
                                                                            patient_id=2+i, timestep=2+i,
                                                                            treatment_options=treatment_options)

    desired=calc_best(patient_history=history, treatment_options=treatment_options,
                                counterfactual_predictions=counterfactual_traj)
    print("treatment paln for ",2+i,treatment_options[desired])

