from flask import Flask
from flask.ext.restful import Resource, Api

import os

app = Flask(__name__)
api = Api(app)

products = [
	'Apples',
	'Bananas', 
	'Carrots'
]


class Catalog(Resource):
	def get(self, product_id):
		if product_id >= len(products):
			return {}, 400
		else:
			return {str(product_id): products[product_id-1]}, 200, {'Server': 'Demo REST API'}

api.add_resource(Catalog, '/catalog/<int:product_id>')

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	host = 'localhost'

	if not port == 5000:
		host = '0.0.0.0'

	app.run(host=host, port=port)