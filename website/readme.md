# ACCT clinical data trial Service Setup

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a AWS EC2 instance.

### Prerequisites

python3 environment for running dashboard

AWS account for deployment

Xshell for connection

WinSCP for file transfer to EC2 instance

```
Give examples
```

### Installing

To be able to run the dashboard project and make connections to aws, packages are needed to install.

```
  pip install django
  pip install boto3
  pip install scikit-learn
  pip install scipy
  pip install sklearn
  pip install PyAthena
  pip install numpy
  pip install awscli
```

And configure local environment for using django and PyAthena, and aws account for using boto3

``` 
  export accessKey='AWSAccessKeyId_HERE'
  export secretKey='AWSSecretKey_HERE'
  export django_access_key='Django_SECRET_KEY_HERE'

  aws configure
  
 [ enter access key and secret key in AWS account
  the region should be us-east-2
  the output format can be json]
```

## Running the tests

Start the server and test dashboard.

```
  python3 manage.py runserver
```

### Test on browser

Open the url in browser and dive to patient page, enter the information in the page as required.

```
  Health Condition: the health condition of the patient, search and multi-selection allowed.
  Treatment: the treatment approached conducted in the clinical trial, search and multi-selection allowed.
```

After clicking on submit button, results will be shown on the bottom of the web page. 

The progress bar shows the probability of encoutering any adverse events based on the personal and clinical trial information provided. The result is retrieved from SageMaker.

If there are some clinical trials which contain similar information as the user, a table will be shown as recommendation and highlights all the adverse events that might occur during the experimental process.

## Deployment

1. Launch EC2 instance(ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-20180306 (ami-916f59f4)) 
2. Specify EC2 security group
  ```
  add HTTP protocol, port number 8000, IP from anywhere.
  add SSH protocol, port number 22
  ```
3. Enter EC2 instance by Xshell, and install dependencies, enter the following commands
```
  sudo apt-get update
  sudo apt-get install python3
  sudo apt-get install python-pip python-dev build-essential 
  ```
  
  if the following command does not allow, add --user at the end of the command
  ```
  pip install django
  pip install scikit-learn
  pip install scipy
  pip install sklearn
  pip install PyAthena
  pup install 
  pip install numpy
  pip install awscli
  aws configure
  
 [ enter access key and secret key in AWS account
  the region should be us-east-2
  the output format can be json]
  
  ``` 
  
4. transfer TiberSolution Folder to instance under the directory /home/ubuntu using WinSCP
5. enter directory /home/ubuntu/TiberSolutions/website/ 
6. open tmux session by entering tmux in the shell
7. make the migrations to check any missing package
    ```
    python3 manage.py makemigrations
    ```
8. run the server
    ```
    python3 manage.py runserver [DNS address]:8000
    ```
9. enter DNS address:8000 in browser, and now your website is running.    


## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

