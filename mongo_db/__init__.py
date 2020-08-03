from flask import Flask, jsonify, Response, render_template, request, flash, redirect
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import json
from wtforms import Form, StringField


'''
Database
'''
DB_NAME = ''
URI = ''

try: 
	open('uri.txt')
	uri_path = 'uri.txt'
except:
	uri_path = 'mongo_db/uri.txt'

with open(uri_path, 'r+') as my_uri:
	DB_NAME = my_uri.readline().strip()
	URI = my_uri.readline().strip()
client =  MongoClient(URI)
db = client[DB_NAME]

'''
Flask
'''
# create an instance of Flask
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# create the API
api = Api(app)
app.secret_key = 'some secret key'


'''
Web App
'''
# create form for search
class Star_Search_Form(Form):
	search = StringField('')

# create form for adding
class Star_Add_Form(Form):
	name = StringField('')
	distance = StringField('')

# load home page
@app.route('/')
def index():
	star_list = Star_List()
	return render_template('home.html', stars=star_list.get()[0]['result'])

# load other pages
@app.route('/<string:page_name>/', methods=['GET', 'POST'])
def page_load(page_name):
	# find item
	if page_name == 'find.html':
		my_search = Star_Search_Form(request.form)
		if request.method == 'POST':
			return search_results(my_search)
		return render_template('find.html', form=my_search)
	
	elif page_name == 'insert.html':
		my_add = Star_Add_Form(request.form)
		if request.method == 'POST':
			return add_results(my_add)
		return render_template('insert.html', form=my_add)

	elif page_name == 'delete.html':
		my_delete = Star_Search_Form(request.form)
		if request.method == 'POST':
			return delete_results(my_delete)
		star_list = Star_List()
		return render_template('delete.html', stars=star_list.get()[0]['result'], form=my_delete)

	elif page_name == 'update.html':
		my_update = Star_Add_Form(request.form)
		if request.method == 'POST':
			return update_results(my_update)
		star_list = Star_List()
		return render_template('update.html', form=my_update, stars=star_list.get()[0]['result'])
		

	return render_template(page_name)


# updating values
def update_results(update):
	star = db.stars
	results = star.update_one({'name': update.data['name']}, {'$set': { 'distance': update.data['distance']}, '$currentDate': {'lastModified': True}})
	if results:
		flash('{} was updated'.format(update.data['name']))
	else:
		flash('Try Again!')
	return redirect('/update.html')


# deleting values 
def delete_results(delete): 
	star = db.stars
	results = star.delete_one({'name': delete.data['search']})
	if results:
		flash('Star removed!')
	else:
		flash('Try Again!')
	return redirect('/delete.html')



# adding values 
def add_results(add):
	star = db.stars
	results = star.insert_one({'name': add.data['name'], 'distance': add.data['distance']})
	if results:
		flash('Star Added!')
	else:
		flash('Try Again!')
	return redirect('/insert.html')



# getting search results
def search_results(search):
	star = db.stars
	results = [ {'name' : s['name'], 'distance' : s['distance']} for s in star.find({'name': search.data['search']})]
	if len(results) == 0: 
		flash('No results found!')
	else:
		for result in results: 
			flash(result)
	return redirect('/find.html')



'''
REST API
'''
class Star_List(Resource):
	def get(self):
		# get the collection
		star = db.stars
		output = [ {'name' : s['name'], 'distance' : s['distance']} for s in star.find()]
		return {'result': output}, 200

	def post(self):
		# get the collection
		star = db.stars

		# parse the arguments
		parser = reqparse.RequestParser()
		parser.add_argument('name', required=True)
		parser.add_argument('distance', required=True)
		args = parser.parse_args()

		# insert the star
		star_id = star.insert_one({'name': args.name, 'distance': args.distance})
		# get the inserted star
		inserted_star = star.find_one({'_id': star_id })
		output = {'name' : inserted_star['name'], 'distance' : inserted_star['distance']}
		return {'result' : output}, 200



class Star(Resource):

	def get(self, name):
		 # get the collection
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
		 # get the collection
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
		# get the collection
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