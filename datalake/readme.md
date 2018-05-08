# Data Lake Setup Instructions

## Overview
The storage layer of our data lake makes use of two AWS services: AWS Lambda and AWS Glue. We use AWS Lambda to run a data crawler daily. It keeps track of the AACT website and ingests newly-posted data into our S3 bucket. Then AWS Glue will scan through the S3 bucket and update the meta data. With the help of these two services, we can persist the raw data in our data lake and interact with the data through AWS Athena.

## Setup AWS S3 Buckets
To run the data crawler, we need to setup two AWS S3 buckets first: one for storing the actual data files and the other one for maintaining additional information to help the crawler find out new data. Both read and write access to these S3 buckets are required. There are many different ways to create buckets in AWS S3. The most intuitive one is using the AWS S3 dashboard webpage. The steps are as the following:

1. Click the 'Create bucket' button.
2. Enter a globally unique bucket name and select a suitable region based on the expected workload.
3. Go to the 'Set properties' tag and grant both read and write access to your account.
4. Click the 'Create bucket' button to finish the process.

## Setup AWS Lambda Functions
Since the data crawler uses third-party packages that AWS Lambda doesn't provide natively, we need to include the packages alongside with our code and pack them as a deployment package.

Right now, the 'lambda\_deployment\_package' folder already contains all the packages the crawler needs and the 'lambda\_deployment\_package.zip' is a compressed file generated from the folder. If you want to use any additional package, you can do it by the following two steps:

1. Install the package you need into the folder by running the following command in current folder: `pip install package_you_need -t lambda_deployment_package`
2. Compress the folder content into a ZIP file by running the following command in current folder: `cd lambda_deployment_package && zip -r lambda_deployment_package.zip *`

Even if you don't need additional package, you may still need to change the target AWS S3 buckets in the code before you run the crawler, because right now the crawler is set to upload files to our demo buckets. In the source code, the target bucket names is assigned by two variables called 'data\_bucket\_name' and 'config\_bucket\_name' in the main function of 'daily\_run.py'. You should change that to the name of the buckets you just create. Make sure to do the second step above to compress a new ZIP file after you modify the source code.

To deploy our code online as an AWS Lambda function, go to the AWS Lambda dashboard webpage and follow these steps:

1. Start creating a new function by clicking the 'Create function' button.
2. Choose 'Author from scratch' mode.
3. Give a name to your function and set the runtime to Python 2.7.
4. Select an IAM role with sufficient permissions. The data crawler in the source code needs to have at least read and write access to AWS S3.
5. Now the function is created, but there's still no function code in the function. Select 'Upload a .ZIP file' from the drop down menu called 'Code entry type' and upload the ZIP file we create before.
7. Click the 'Save' button. You can also click the 'Test' button on the left to test running our function. After the running completes, you should be able to see the data files in your S3 buckets.

Now we have an AWS Lambda function that can download a new data file from the target website every time it runs. To automate the data crawling process, we need to make use of the CloudWatch Events. It works similarly to a job scheduler. You can setup a CloudWatch Events follow the steps below:

1. Go to the AWS Lambda dashboard webpage and click the function name into the function detailed page.
2. Expand the 'Designer' tab and add a new trigger. Select 'CloudWatch Events' from the drop-down menu on the left side.
3. In the 'Configure triggers' box, select 'Create a new rule' from the 'Rule' drop-down menu.
4. Enter a rule name and rule description.
5. Choose 'Schedule expression' as the rule type. Express the expected schedule in either Cron expressions or rate expressions.
4. Check the 'Enable trigger' box and click the 'Add' button. The CloudWatch Event is up and running now.

## Setup AWS Glue Data Catalog
Although we can interact with the data using SQL, there's no actual database under the hood. The data scanning is performed directly on the raw text files in the S3 bucket. To speed up the scanning process, we need some extra meta data maintained for the data lake. AWS provides a convenient service called AWS Glue to help build up the meta data. After the data crawler ingests new data into the S3 buckets, AWS glue will scan through the S3 bucket and update the meta data.

To provide a concept of 'database' in our datalake, we need to create a conceptual database on our S3 bucket first. This can be done by the following two steps:

1. Go to the AWS Glue dashboard and choose 'Databases' from the left column.
2. Click the 'Add database' button. Type in the name of the database and create it.

Once we finish creating the database, we can add tables into it. We use the crawler provided by the AWS Glue to detect the table relations in the S3 bucket automatically. Different from our data crawler that runs on AWS Lambda, which downloads the data from the target website and upload them into our S3 buckets, the crawler provided by AWS Glue will scan the S3 buckets you choose  and build meta data based on the bucket content. By default, it treats each folder in the bucket as a table. Do the following steps on the AWS Glue dashboard:

1. Choose 'Tables' from the left column.
2. Click the 'Add tables' button. Choose 'Add tables using a crawler'.
3. Enter a name for the crawler. Go to 'Next'.
4. Choose 'S3' in the 'Data store' drop-down menu.
5. Choose 'Specified path in my account'.
6. Enter the path of the S3 buckets and go to 'Next'
7. Choose or create an IAM role that have full accesses to AWS Glue and S3.
8. Select 'Daily' as the running frequency.
9. Select the database we just create as the output database.
10. Click 'Finish' and go back the AWS Glue dashboard.
11. If we want to manually start the first run immediately, we can select the crawler we just create and click 'Run crawler'.

## Use AWS Athena to Interact with Data
After setting up the AWS Lambda crawler and AWS Glue, the storage layer of our data lake has been built successfully. We can use AWS Athena to execute SQL statements directly on our data lake now. For a quickly exploration in our data, we can follow these steps:

1. Go to AWS Athena dashboard webpage.
2. Select the database we built in AWS Glue.
3. Type in the SQL statement we want in the editor and click 'Run query'.

Besides Athena, AWS Quicksight is also a good tool for data exploration. It can provide easy visualization for our data lake.

