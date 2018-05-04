# Data Lake Setup Instructions

## Overview
Our data lake storage layer consists of two parts: AWS Lambda and AWS Glue. AWS Lambda keeps track of the AACT website and ingests the newly-posted data into our S3 bucket, while AWS Glue scans through our S3 bucket every day and updates the meta data whenever new data comes in. With the help of these two services, we can persist the raw data in our data lake and interact with the data through AWS Athena.

## Setup AWS S3 Buckets
In our data lake, there are two different bucket: one for storing the actual data files and the other one for maintaining additional information for the crawler. We need to setup two buckets and make sure we have both read and write access to the bucket. There many different ways to create buckets in AWS S3. The easiest one is to create them through AWS console webpage.

## Setup AWS Lambda Functions
Since our crawler uses third-party packages that AWS Lambda doesn't provide natively, we need to include the packages alongside with our code and pack them as a deployment package. Right now, the 'lambda\_deployment\_package' folder already contains all the packages the crawler needs and the 'lambda\_deployment\_package.zip' is the compressed file generated from the folder. If you want to use any additional package, you can do it by the following two steps:

1. Install the package you need into the folder by running the following command in current folder: `pip install package_you_need -t lambda_deployment_package`

2. Compress the folder content into a ZIP file by running the following command in current folder: `cd lambda_deployment_package && zip -r lambda_deployment_package.zip *`

Even if you don't need additional package, you may need to change the target AWS S3 bucket the code before you run the crawler. The target bucket names is assigned by two variables called 'data\_bucket\_name' and 'config\_bucket\_name' in the main function of 'daily\_run.py'. You should change that to the name of the buckets you create. Make sure to do the second step above to compress a new ZIP file after you modify any content in the folder.

To deploy our code as an AWS Lambda function, go to the AWS Lambda dashboard webpage and follow these steps:

1. Start creating a new function by clicking the 'Create function' button.
2. Choose 'Author from scratch' mode.
3. Give a name to your function and set the runtime to Python 2.7.
4. Select an IAM role with sufficient permissions. Our crawler here needs to have at least read and write access to S3.
5. Now the function is created, but there's still no function code. Select 'Upload a .ZIP file' from the drop down menu called 'Code entry type' and upload the ZIP file we create before.
6. Click the 'Save' button.

