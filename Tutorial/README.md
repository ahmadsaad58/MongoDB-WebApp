title: Creating a Web Application and REST API with MongoDB and Python

## Why Python?
When we talk about web programming, Python is not the first thing we think of. For designing our front end, we think *Javascript*, *HTML*, and *CSS*. We think *Java*, *Go* or *NodeJS* for our back end. Python is often relegated to data sciences and machine learning, but this dynamically typed and interpreted language can serve many purposes with the right libraries/modules. Before we can jump in with Python, we must install and get it running! You can use the README from my [GitHub Repo](https://git.target.com/SaadAhmad/Mongo-Rest) to do this.

## Python and the Web
As I mentioned earlier, Python is a very versatile language. With the right libraries, we can serve a full stack web app and REST API. For this tutorial, we will be using **Flask, Flask-Restful, and PyMongo**. For our front end, we will be using *Jinja* as our templating engine and *Bootstrap* to make our web app dynamic. All of my code and these dependencies are available on the README from my [GitHub Repo](https://git.target.com/SaadAhmad/Mongo-Rest). Now, let's jump into the different libraries!

## Rest API
First, we will create our REST API to interact with our Mongo instance. We will them create the web app to visualize and test some of our changes.

### Flask and Flask-Restful
To build web applications in Python, there are many frameworks we could use. For this tutorial we are going to focus on Flask. Flask is a micro web framework for Python. Flask's mission it to keep things simple and acessible to get applications up and running very quickly. Flask also does not make many decisions for you instead it supports different libraries to add functionality. If you are new to Flask or web development, this [documentation](https://flask.palletsprojects.com/en/1.1.x/) will help greatly.

Before we jump further into this tutorial, let's try out the hello world tutorial from the [Flask Quickstart Guide](https://flask.palletsprojects.com/en/1.1.x/quickstart/)

```python
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

```

To test this endpoint, we can use cURL or our favorite browser, but to save us time and simplifiy some complexity, we will use a REST client to test our methods. In this tutorial, I will use [Insomnia](https://insomnia.rest/) but [Postman](https://www.postman.com/) or your favorite REST client work the same.

To test our endpoint, we must run the script by typing in our terminal ```python3``` followed by the python file. In my case, I would type ```python3 hello-world.py```. This is what my terminal looks like:

![Image of my Terminal](images/hello-world-terminal.png)

When the server is running, you will get a local development IP (mine is http://127.0.0.1:5000/) that you can follow to the endpoint.

This is how the endpoint looks on my browser:

![Image of my Browser](images/hello-world-browser.png)

This is how it looks on Insomnia:

![Image of Insomnia](images/hello-world-insomnia.png)

We can build onto this by importing more libraries and adding logic to our endpoints. Let's do that now! We are going import *Flask-Restful*, a lightweight extension to help us make our REST-API with ease while encouraging the best practices. You can always use vanilla Flask if you do not want to use *Flask-Restful*.

**Let's extend what we wrote earlier:**
```python
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

    # overwrite the GET method and return a valid status code
    def get(self):
        status_code = 200
		return {'Result': 'Some Result as JSON'}, status_code

    # overwrite the Post method
	def post(self):
		# parse your query parameters
		parser = reqparse.RequestParser()
		parser.add_argument('arg1', required=True)
		parser.add_argument('arg2', required=True)
		args = parser.parse_args()
        status_code = 200
		return {'arg1' : args.arg1, 'arg2' : args.arg2}, status_code


# add the resource we created to an endpoint
api.add_resource(My_Resource, '/my_resource')

if __name__ == '__main__':
    app.run(debug=True)
```

Let's test it! Just like last time, run the script and load the IP!

![Not Found](images/not-found-flask-restful.png)

What's this? It was not found because we did not route a resource to that function! Let's try again:

![Found](images/found-flask-restful.png)

Let's try our POST method now using Insomnia, with the query parameters as ```arg1=hello``` and ```arg2=world```. This is our endpoint: http://127.0.0.1:5000/my_resource?arg1=hello&arg2=world

![Post Flask-Restful](images/flask-restful-post.png)

We can continue to write more classes and methods to create more resources and HTTP methods for those endpoints. The full code for the resources I created are on my [GitHub Repo](https://git.target.com/SaadAhmad/Mongo-Rest).

### PyMongo
As I mentioned earlier, Flask keeps things simple out of the box but can allow for more functionality by importing a variety of libraries. To add functionality for Mongo, we will import Pymongo to connect to and interface with our remote Mongo instance. For more Mongo documentation, use the [Mongo Manual](https://docs.mongodb.com/manual/) to get started.

To connect to your Mongo instance, you need to create a URI with the correct credentials. Here is a sample URI you can insert you credentials into: ```mongodb://my_username:my_password@my_host:27017/?authSource=authentication```

To check if your credentials are correct, try logging into your Mongo instance via Terminal by typing ```mongo "{your URI}"``` (**do not forget the quotes around your URI**).

Once you have verified you can connect to your instance, we can proceed to integrate Mongo into our web app and REST API. Use the [Mongo Manual CRUD Operations](https://docs.mongodb.com/manual/crud/) to get started with inserting and retrieving.

The Mongo Manual even provides tutorials via a built in Mongo Shell and code snippets for PyMongo.

**Let's continue to extend what we wrote earlier with the help of the Mongo Manual:**
```python
from flask import Flask
from flask_restful import Resource, Api, reqparse
# import MongoClient to connect to remote Mongo Instance
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
app.secret_key = 'some secret key'

# insert URI that you created here
URI = 'mongodb://my_username:my_password@my_host:27017/?authSource=authentication'
# Database you are storing values to
DB_NAME = 'my_database'
# connect
client =  MongoClient(URI)
db = client[DB_NAME]

class My_Resource(Resource):
    def get(self):
        # get the collection
        collection = db.my_collection
        # use the find command (check out the Mongo Manual for more info)
		output = [ {'arg1' : s['arg1'], 'arg2' : s['arg2']} for s in collection.find()]
        status_code = 200
		return {'Result': output}, status_code

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('arg1', required=True)
		parser.add_argument('arg2', required=True)
		args = parser.parse_args()

        # get the collection
        collection = db.my_collection
        # insert the item and get item ID
		item_id = collection.insert_one({'arg1': args.arg1, 'arg2': args.arg2})
        # find inserted item
        inserted_item = collection.find_one({'_id': item_id })
        status_code = 200
		return {'arg1' : inserted_item['arg1'], 'arg2' : inserted_item['arg2']}, status_code

api.add_resource(My_Resource, '/my_resource')

if __name__ == '__main__':
    app.run(debug=True)
```

We can continue to add more methods and endpoints to interact with our Mongo instance. We can add a whole host of CRUD functionality to our REST API. I have implemented some more functions and they are available on my [GitHub Repo](https://git.target.com/SaadAhmad/Mongo-Rest). To test our REST API, we can use our REST Client or build a web application to help us visualize the changes we make to our Mongo database.

## Web Application
What is a web app? To keep things simple, we can think of a web application as a program that runs on a web server and can be accessed by a HTTP connection. Since we are building this app, the web server will be our computer and we will use a browser to access the HTTP connection. To test it, we can use the browser to help us with the front end and the REST API to test if we are correctly interacting with our Mongo instance.

### Templating and Back end
When it comes to web applications, we need to pass information from our back end to our front end to present it to our user. For this, we need a templating engine. Flask provides us with [Jinja](https://jinja.palletsprojects.com/en/2.11.x/), a fast and designer-friendly templating language.

To start with templates, we must create a ```templates``` folder to store all of our template files (HTML files). We must also modify our code to direct the Flask app to the location of our templates. **Change this line to include our templates:**

<s>```app = Flask(__name__)```</s>

```app = Flask(__name__, template_folder='templates')```

Now, let's create a simple HTML page that the other templates can extend. We can call this page the layout page. Here we can add components that will be present in all of the pages of our web app such as a navbar or footer.

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Web App</title>
</head>
<body>
    {% block body %}{% endblock %}
</body>
</html>
```

For now this looks like a simple HTML page but upon closer inspection, you see the line containing ```{% block body %}{% endblock %}```. This is part of Jinja and allows other templates to fit right in between. This layout file will us save us some time in the future since we no longer have to rewrite an entire HTML file, we can write smaller blocks that can fit in between the body and end blocks. This will also prevent us from copy pasting.

In order for our web app to route us to the correct pages, we must add endpoints to our back end. We will **not** use Flask-Restful for this, instead we will add an anotation like we did in the *hello-world example* earlier. It should look like this:

```python
@app.route('/')
def index():
	return render_template('home.html')

# to route to pages based on name
@app.route('/<string:page_name>/')
def load_page(page_name):
    return render_template(page_name)
```

**Now let's move onto an example of a template that extends our layout:**

```html
{% extends 'layout.html' %}
{% block body %}
<h1>Welcome to Item Database</h1>
{% endblock %}
```

This file should also be saved as an HTML file. Notice how it first extends the layout and then adds the ```h1``` tag for a title. When it loads in the browser, we can see that this page loads as the layout HTML but with the ```{% block body %}{% endblock %}``` is replaced with ```<h1>Welcome to Item Database</h1>```

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Web App</title>
</head>
<body>
    <h1>Welcome to Item Database</h1>
</body>
</html>
```

To pass information between the web page and the template, we can add another parameter in the ```render_template``` function with the values we want available on that page. We can get these values from our database by calling the suitable Mongo function.

```python
@app.route('/<string:page_name>/')
def load_page(page_name):
    collection = db.my_collection
    items = [ {'arg1' : s['arg1'], 'arg2' : s['arg2']} for s in collection.find()]
    return render_template(page_name, items=items)
```

Now you can list all the items using Jinja by looping through the items that were passed to the front-end. We can use loops to show all our items or list messages. There are more examples on my [GitHub Repo](https://git.target.com/SaadAhmad/Mongo-Rest).

```html
<h1> The Items are: </h1>
<ul>
    {% for item in items %}
    <li>
        {{item.arg1}}, {{item.arg2}}
    </li>
    {% endfor %}
</ul>
```

### Extensions
We can extend our templating with forms using a variety of libraries available to Flask. We can also make the web page responsive by adding Bootstrap. In my [GitHub Repo](https://git.target.com/SaadAhmad/Mongo-Rest), I added Bootstrap by linking to the online Javascript files and by using local CSS files. You can link online CSS files without too much hassle and add classes and wrappers to the templates to make the page more responsive. I also added a navbar to my layout file using the *includes statement*: ```{% include 'includes/_navbar.html' %}```. This will help users navigate the web app more easily. This is just scratching the surface of what can be done with the web app.

## Testing
Now that we have both our API and web app up and running, we can easily test and visualize interactions with our Mongo instance! We can add items through the API and see it on the web app or vice versa. We can use our API with scripts to bulk add or remove or we could use easily interface with our web app. I did not unit or functionally test my API but that could be something you could do for your app. I hope this tutorial helped you learn something!
