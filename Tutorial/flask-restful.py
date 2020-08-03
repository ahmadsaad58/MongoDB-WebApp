from flask import Flask
# import flask-restful to create our api
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

# create the api from the app
api = Api(app)
# add a string secret (can be anything)
app.secret_key = 'some secret key'

# define a class that extends the Resource class to overload HTTP Methods
class My_Resource(Resource):

    # overload the GET method and return a valid status code
    def get(self):
        status_code = 200
        return {'Result': 'Some Result as JSON'}, status_code

    # overload the Post method
    def post(self):
        # parse your query parameters
        parser = reqparse.RequestParser()
        parser.add_argument('arg1', required=True)
        parser.add_argument('arg2', required=True)
        args = parser.parse_args()
        status_code = 200
        return {'arg1' : args.arg1, 'arg2' : args.arg2}, status_code


# add the resource we created
api.add_resource(My_Resource, '/my_resource')

if __name__ == '__main__':
    app.run(debug=True)
