# import flask to use it
from flask import Flask

# make the flask app
app = Flask(__name__)

# routing our first endpoint
@app.route('/')
def hello_world():
    return 'Hello World!'

# we run the app under this block to prevent it from running in other modules/files
if __name__ == '__main__':
    # setting debug to True allows the server to automatically reload
    app.run(debug=True)
