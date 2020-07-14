# Welcome to the Mongo Rest Client 

This REST-API provides CRUD operations for a *Mongo Database*
1. Create Resource
2. Retrieve Information
3. Update Information
4. Delete Resource


## Get your Environment Setup (optimized for Linux and MacOS)

Before we jump in, you'll need a couple of things for this to work:

Python 3.7.7 with packages: 
- Flask (version 1.1.2)
- Flask-RESTful (version 0.3.8)
- PyMongo (version 3.10.1)
- Flask-PyMongo (version 2.3.0)
- WTForms (version 2.3.1)

 **(You can do this by following one of the methods)** 

1. Use vanilla **Python 3.7.7 (latest python 3.7 version)** and pip3 on MacOS: 
    1. `brew install Python3` to install python 
    2. `python3 --version` to verify you have *python 3.7.7*
    2. `pip3 install -r requirements.txt` to get the packages needed for this script


*I highly recommend using Anaconda to manage Python environments:*

2. Use **Anaconda**:
    1. Download Anaconda and [Get Started with Environments](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)
    2. `conda create --name [name] python=3.7.7` to create the environment
    3. `conda activate [name]` to activate said environment
    4. `pip install -r requirements.txt` to install the packages


## Connecting to Mongo Instance

In order to run this web app, you must add a `uri.txt` to the mongo_db folder. This file will contain the login and database info you are trying to access

*The sample_uri.txt provides a good example*

**Follow this format strictly or risk having the script crashing**

`On line 1:` add the database name you are trying to access 

`On line 2:` add the connection string to access the mongo cluster. To format the URI follow [this guide](https://docs.mongodb.com/manual/reference/connection-string/)


## Running Server 
`python3 app.py` will run the server on [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

Endpoints are `/stars` and `/stars/<name>`