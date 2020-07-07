# Mongo-Rest

## Welcome to the Mongo Rest Client 

This REST-API provides CRUD operations for a *Mongo Database*
1. Create
2. Read
3. Update
4. Delete


### Get your Environment Setup

Before we jump in, you'll need a couple of things for this to work:

Python 3.7 with packages: 
- Flask (version 1.1.2)
- Flask-RESTful (version 0.3.8)
- PyMongo (version 3.10.1)
- Flask-PyMongo (version 2.3.0)
- WTForms (version 2.3.1)

 **(You can do this by following one of the methods)** 

1. Use vanilla **Python 3.7.7** and pip3 on MacOS: 
    1. `Brew install Python` to install python 
    2. `python --version` to verify you have *python 3.7*
    2. `pip3 install -r requirements.txt` to get the packages needed for this script


*I highly recommend using Anaconda to manage Python environments:*

2. Use **Anaconda**:
    1. Download Anaconda and [Get Started with Environments](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)
    2. `conda create --name [name] python=3.7.7`
    3. `conda activate [name]`
    4. `pip install -r requirements.txt`


In order to run this web app, you must add `uri.txt` to the mongo_db folder. This file must have on **line 1: DB_Name** and on **line 2: the mongo login string** 


