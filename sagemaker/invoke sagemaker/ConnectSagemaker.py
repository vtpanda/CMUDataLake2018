import math
# boto3 configuration: http://boto3.readthedocs.io/en/latest/guide/configuration.html
# for local machine, finish 'aws configure' with AWS CLI is sufficient
import boto3
import numpy as np
from sklearn.feature_extraction import FeatureHasher
import os
import io
import json


def np2csv(arr):
    csv = io.BytesIO()
    np.savetxt(csv, arr, delimiter=',',fmt='%s')
    return csv.getvalue().decode().rstrip()

def sigmoid(x):
    
    return 1.0 / (1.0 + math.exp(-x))

def invoke_sagemake_endpoint(input_features, sagemaker_endpoint_name, 
                             number_of_conditions=1909, number_of_interventions=1846, number_of_countries=142):
    """
    send a query to AWS sagemaker endpoint which host the ML model that is already trained.
    
    Args:
        input_features (list): [number_of_facilities(integer), 
                                has_us_facility(integer: 0 or 1), 
                                number_of_sponsors(integer), 
                                [list_of_strings](conditions), 
                                [list_of_strings](interventions), 
                                country(string)]
        sagemaker_endpoint_name (str): The sagemaker endpoint name. (e.g. linear-learner-2018-04-13-19-47-11-302)
        number_of_conditions (int): total number of conditions 
        number_of_conditions (int): total number of interventions
        number_of_conditions (int): total number of countries

    Returns:
        float: The probability that a clinical trial will cause serious adverse reaction, given input features.
    """
    
    
    # read in the conditions, interventions and countries catagories
#     unique_conditions = np.load('conditions_catagories.npy')
#     unique_interventions = np.load('interventions_catagories.npy')
#     unique_countries = np.load('countries_catagories.npy')
    
    # feature hasher
    conditions_hasher = FeatureHasher(n_features=int(number_of_conditions * 0.2),
                                                                 non_negative=True,input_type='dict')
    interventions_hasher = FeatureHasher(n_features=int(number_of_interventions * 0.2),
                                                                 non_negative=True,input_type='dict')
    countries_hasher = FeatureHasher(n_features=int(number_of_countries),
                                                                 non_negative=True,input_type='dict')
    # input feature transform to feature hasher input format
    conditions_dict = {}
    for condition in input_features[3]:
        conditions_dict[condition] = 1
        
    interventions_dict = {}
    for intervention in input_features[4]:
        conditions_dict[condition] = 1
    
    contry_dict = {}
    contry_dict[input_features[5]] = 1
    
    hashed_condition_features = conditions_hasher.transform([conditions_dict]).toarray()
    hashed_intervention_features = interventions_hasher.transform([interventions_dict]).toarray()
    hashed_country_features = countries_hasher.transform([contry_dict]).toarray()
    
    
    # feature vector: 
    # number_of_facilities, has_us_facility, number_of_sponsors, 
    # conditions_features, interventions_features, contries_features
    feature_vector = []
    feature_vector.append(input_features[0])
    feature_vector.append(input_features[1])
    feature_vector.append(input_features[2])
    feature_vector += hashed_condition_features[0].tolist()
    feature_vector += hashed_intervention_features[0].tolist()
    feature_vector += hashed_country_features[0].tolist()
    feature_vector = np.array(feature_vector).reshape(1, -1)
    print('feature_vector shape: {}'.format(feature_vector.shape))
    
    # invoke the endpoint
    runtime = boto3.Session().client(service_name='runtime.sagemaker',region_name='us-east-2')
    response = runtime.invoke_endpoint(EndpointName=sagemaker_endpoint_name, \
    ContentType='text/csv', \
    Body=np2csv(feature_vector))
    result = response['Body'].read()
    score = json.loads(result)['predictions'][0]['score']
    # map the score to (0,1) probability using sigmoid functions
    return sigmoid(score)
    

if __name__== "__main__":
    # example
    endpoint_name = 'linear-learner-2018-04-20-05-01-38-054'
    sample_input_feature = [10, 1, 10, ['diabetes mellitus', 'diabetes mellitus, type 2'], 
                        ['antibodies, monoclonal', 'methotrexate'], 'United States']
    print(invoke_sagemake_endpoint(sample_input_feature, endpoint_name))
