from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo

# mongodb://localhost:27017/

DB_NAME = 'mongo_test'
URI = ''
with open('uri.txt', 'r+') as my_uri:
	URI = my_uri.readline().strip()

# create an instance of Flask 
app = Flask(__name__) 

# config the app
app.config['MONGO_DBNAME'] = DB_NAME
app.config['MONGO_URI'] = URI + DB_NAME

# create the API 
api = Api(app)

# create the mongo app
mongo = PyMongo(app)


# intro page
@app.route('/')
def index():
	return 'Welcome to Mongo DB Rest Client'


class StarList(Resource):
	def get(self):
		# get the db
		star = mongo.db.stars
		output = [ {'name' : s['name'], 'distance' : s['distance']} for s in star.find()]
		return jsonify({'result' : output})

	def post(self):
		# get the db
		star = mongo.db.stars
		
		# parse the arguments
		parser = reqparse.RequestParser()
		parser.add_argument('name', required=True)
		parser.add_argument('distance', required=True)
		args = parser.parse_args()

		# insert the star
		star_id = star.insert({'name': args.name, 'distance': args.distance})
		# get the inserted star
		inserted_star = star.find_one({'_id': star_id })
		output = {'name' : inserted_star['name'], 'distance' : inserted_star['distance']}
		return jsonify({'result' : output})



class Star(Resource):

	def get(self, name):
		 # get the db
		star = mongo.db.stars
		
		# find the star
		s = star.find_one({'name' : name}) 
		# format output
		output = {'name' : s['name'], 'distance' : s['distance']} if s else 'No such name'
		return jsonify({'result' : output})



# add resources
api.add_resource(StarList, '/stars')
api.add_resource(Star, '/star/<name>')


if __name__ == '__main__':
	app.run(debug=True)