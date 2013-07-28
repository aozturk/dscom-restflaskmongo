from flask import Flask
from flask.ext.restful import Resource, Api, reqparse

import os

# the application instance
app = Flask(__name__)
# the api instance
api = Api(app)

# the 'database'
products = [
	'Apples',
	'Bananas', 
	'Carrots'
]


class Catalog(Resource):
	def __init__(self):
		# the only argument that is passed through the request body
		# is product_name and it is not required
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('product_name', type=str)
		self.args = self.parser.parse_args()

	def get(self, product_id):
		# indexes out of range are invalid requests, return status 400
		if product_id > len(products):
			return {}, 400
		else:
			# the product_id is 1 indexed but the 'database' is zero
			# indexed so account for the off by one
			return {str(product_id): products[product_id-1]}, 200, {'Server': 'Demo REST API'}

	def put(self):
		# get the product name out of the parsed request body
		product_name = self.args['product_name']
		# add it to the 'database'
		products.append(product_name)
		# return the new product_id
		return {str(len(products)): product_name}, 201, {'Server': 'Demo REST API'}

	def delete(self, product_id):
		# check if the request is valid
		if product_id > len(products):
			return {}, 400
		else:
			# set the product_id to blank to ensure that
			# existing product_id's don't change
			products[product_id-1] = ''
			return {}, 204, {'Server': 'Demo REST API'}

class CatalogAPI(Resource):
	def get(self):
		# get a list of all product_id's whose names are not blank
		return {
			'products': [
				{str(x+1): products[x]} for x in range(len(products)) if not products[x] == ''
			]
		}

# you don't have to specify the HTTP verb for each add_resource call
# since the Resource class will call the appropriate method
# for multiple endpoints mapped to the same Resource class
# order them in most specific to most generic
api.add_resource(Catalog, '/catalog/<int:product_id>')
api.add_resource(Catalog, '/catalog')
api.add_resource(CatalogAPI, '/catalogapi')

if __name__ == '__main__':
	# most of this is for hosting on Heroku
	# several times while testing I orphaned
	# a server process and had to change the port
	# I was testing on so I added this default_port
	# which is used locally only
	default_port = 5001
	port = int(os.getenv('PORT', default_port))

	host = 'localhost'
	debug = True

	if not port == default_port:
		host = '0.0.0.0'
		debug = False

	app.run(host=host, port=port, debug=debug)