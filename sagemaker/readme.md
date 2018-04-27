# Sagemaker Deployment
In this experiment, we provide a demo of predict the risk of a clinical trial (evaluated by percentage of having adverse reactions) using the pre-cleaned [AACT data](https://aact.ctti-clinicaltrials.org/pipe_files) we loaded in AWS Athena.

We are going to build a Linear Regression Model using AWS Linear Learner using AWS Sagemaker.

## Prerequisite
To understand our sagemaker experiment, it's better to have knowledge of Python, Jupyter notebook, and SQL Syntax, because:
1. The data is extracted from AWS Athena using SQL
2. The model deployment routine was written in Python Script with Jupyter notebook 

## Amazon Sagemaker:
Amazon SageMaker is a fully-managed platform that enables developers and data scientists to quickly and easily build, train, and deploy machine learning models at any scale. Amazon SageMaker removes all the barriers that typically slow down developers who want to use machine learning.

![alt text](./images/technology_components.PNG)

## File Structure:
data:
- Data used for training the model and the SQL Query used to extract data from AWS Athena

invoke sagemaker:
- Utilities for invoking sagemaker

model:
- Jupyter notebook containing model defination and trainig experiment routine

## Code Deployment:
In the following steps we will introduce how to launch a notebook instance to hold our development environment, run model training jobs and deploy a model on a Endpoint instance.
1. Create Notebook instance. (Steps are [here](https://docs.aws.amazon.com/sagemaker/latest/dg/gs-setup-working-env.html))
2. In the Notebook section, click on "open" under "Actions", this will bring you to the Jupyter notebook page.
3. Upload the "baseline model.ipynb" in the "model" directory and "ordered_ex1_train.csv" to the Jupyter notebook.
4. On Jupyter notebook, open the notebook, and run the [notebook code](note book link) step by step. (Description and comments inline)

Until now you already have:
1. A running Sagemaker notebook instance, you can choose to stop or delete it based on budgets and needs.
2. A Learned Model, you can access it from "Models" section on Sagemaker Console.
3. A Endpoint Configuration, this is the configuration for the Endpoint instance. you can access it from "Endpoint configurations" section on Sagemaker Console. You can modify this configuration, for example, you can change the Endpoint instance type and the model that Endpoint will be holding.
4. A Running Endpoint, you can access it from "Endpoints" section on Sagemaker Console. you can choose to delete it based on budgets and needs.

note: We also recommend watch [this](https://www.youtube.com/watch?v=ym7NEYEx9x4) video before trying the code.

## Resource Management
1. Notebook Instance: You may choose to stop the notebook and start it when you need it to save budget.
2. Models: You may choose to delete your model to free some space on your S3. (Model file is not that large though).
3. You may want to only Endpoint when you need it depend on performance requirement. for experiment purpose we mainly use t2.medium and t2.micro here. 
4. You can also refer to [Sagemaker Pricing](https://aws.amazon.com/sagemaker/pricing/) to better control budget.

# Reference:
[AWS Sagemaker Frontpage](https://aws.amazon.com/sagemaker/?nc1=h_ls)

[AWS Sagemaker github repo](https://github.com/awslabs/amazon-sagemaker-examples)

[Sagemaker Review Vedio](https://www.youtube.com/watch?v=ym7NEYEx9x4)

[API References](https://docs.aws.amazon.com/sagemaker/latest/dg/API_Reference.html)

# More Readings
[Using Your Own Algorithms with Amazon SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms.html)

[Using Your Own Training Algorithms](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo.html)

