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


# IN THE NEXT PART LOAD THE DATA SET AND FORMAT IT AS NEEDED

from datasets.data_loader import CSVLoader

# Define data name
data_name = 'machine_1'
# Define data dictionary
data_directory = '../datasets/data/'+data_name + '/' + data_name + '_'

# Load train and test datasets
data_loader_training = CSVLoader(static_file=data_directory + 'static_train_data.csv.gz',
                                 temporal_file=data_directory + 'temporal_train_data_eav.csv.gz')

data_loader_testing = CSVLoader(static_file=data_directory + 'static_test_data.csv.gz',
                                temporal_file=data_directory + 'temporal_test_data_eav.csv.gz')

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
metric_name = 'auc' #optimize the Area Under Curve
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
                  'encoder_fc_hidden_units':128,
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

