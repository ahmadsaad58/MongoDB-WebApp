from flask import Flask, jsonify, Response, render_template, request, flash, redirect
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
from pymongo import MongoClient
import json
from wtforms import Form, StringField


# create form
class Star_Search_Form(Form):
	search = StringField('')


DB_NAME = ''
URI = ''
with open('uri.txt', 'r+') as my_uri:
	DB_NAME = my_uri.readline().strip()
	URI = my_uri.readline().strip()
client =  MongoClient(URI)
db = client[DB_NAME]

# create an instance of Flask
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# create the API
api = Api(app)
app.secret_key = 'some secret key'


@app.route('/results.html')
def search_results(search):
	star = db.stars
	results = [ {'name' : s['name'], 'distance' : s['distance']} for s in star.find({'name': search.data['search']})]
	if len(results) == 0: 
		flash('No results found!')
	else:
		for result in results: 
			flash(result)
	return redirect('/find.html')



# load home page
@app.route('/')
def index():
	return render_template('home.html')

# load other pages
@app.route('/<string:page_name>/', methods=['GET', 'POST'])
def page_load(page_name):
	# show all results
	if page_name == 'show.html':
		star_list = Star_List()
		return render_template(page_name, stars=star_list.get()[0]['result'])

	# find item
	if page_name == 'find.html':
		my_search = Star_Search_Form(request.form)
		if request.method == 'POST':
			return search_results(my_search)
		return render_template('find.html', form=my_search)


	return render_template(page_name)


class Star_List(Resource):
	def get(self):
		# get the db
		star = db.stars
		output = [ {'name' : s['name'], 'distance' : s['distance']} for s in star.find()]
		return {'result': output}, 200

	def post(self):
		# get the db
		star = db.stars

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
		return {'result' : output}, 200



class Star(Resource):

	def get(self, name):
		 # get the db
		star = db.stars
		# find the star
		s = star.find_one({'name' : name})
		# if not there
		if not s:
			return Response(json.dumps({'result' : '{} was not found'.format(name)}), status=404)
		# format output
		output = {'name' : s['name'], 'distance' : s['distance']}
		return {'result' : output}, 200

	def delete(self, name):
		 # get the db
		star = db.stars
		# delete
		delete_result = star.delete_one({'name': name})
		# get number deleted
		count = delete_result.deleted_count
		# if nothing deleted
		if count == 0:
			return Response(json.dumps({'result' : '{} was not found'.format(name)}), status=404)
		# format output
		return {'result' : '{} has been deleted'.format(name), 'count': count}, 200

	def put(self, name):
		# get the db
		star = db.stars
		# parse the arguments
		parser = reqparse.RequestParser()
		parser.add_argument('distance', required=True)
		args = parser.parse_args()
		# update
		s = star.update_one({'name': name}, {'$set': { 'distance': args.distance}, '$currentDate': {'lastModified': True}})
		# if not there
		if s.matched_count == 0:
			return Response(json.dumps({'result' : '{} was not found'.format(name)}), status=404)
		if s.modified_count == 0:
			return Response(json.dumps({'result' : '{} was not modified'.format(name)}), status=304)
		# format output
		return {'result' : '{} has been modified'.format(name), 'modified count': s.modified_count, 'matched count': s.matched_count}, 200




# add resources
api.add_resource(Star_List, '/stars')
api.add_resource(Star, '/star/<name>')


if __name__ == '__main__':
	app.run(debug=True)