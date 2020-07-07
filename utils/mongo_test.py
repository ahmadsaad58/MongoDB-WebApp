from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
import os

URI = ''
with open('mongo_db/uri.txt', 'r+') as my_uri:
	URI = my_uri.readline().strip()

# Configure the Flask application to connect with the MongoDB server
app = Flask(__name__)
# app.config["MONGO_URI"] = 
# app.config['MONGO_DBNAME'] = 'mongo_test'
# app.config['SECRET_KEY'] = 'secret_key'
client = MongoClient(URI)
print(client.list_database_names())

# Connect to MongoDB using Flask's PyMongo wrapper
# mongo = PyMongo(app)
db = client.mongo_test
print(db)
col = db["stars"]
if not col: 
    col = 'No Collection of that name'
print ("MongoDB Database:", db)

# Declare an app function that will return some HTML
@app.route("/")
def connect_mongo():

    # Setup the webpage for app's frontend
    html_str = '''
    <!DOCTYPE html>
    <html lang="en">
    '''

    # Have Flask return some MongoDB information
    html_str = html_str + " Testing if you are able to connect to MongoDB \n "
    html_str = html_str + " ### " + str(db) + " "
    html_str = html_str + " ### " + str(col) + " "

    # Get a MongoDB document using PyMongo's find_one() method
    html_str = html_str + "</html>"

    return html_str

if __name__ == '__main__':
    app.run(debug=True)