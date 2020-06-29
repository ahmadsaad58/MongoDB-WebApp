from flask import Flask
from flask_restful import Resource, Api, reqparse



# create an instance of Flask 
app = Flask(__name__) 

# create the API
api = Api(app)


