conditions_catagories.npy
countries_catagories.npy
interventions_catagories.npy

numpy arrays containing the categories of conditions, interventions and countries

usage: 
import numpy as np
unique_conditions = np.load('conditions_catagories.npy')

============================================================
ConnectSagemaker.py

utilities for the function of invoke sagemaker

usage: 
from ConnectSagemaker import invoke_sagemake_endpoint

print(invoke_sagemake_endpoint(sample_input_feature, endpoint_name))


note: make sure sklearn and boto3 is installed

