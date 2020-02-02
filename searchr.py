import scraper
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('search_term')

class SearchResults(Resource):
    def get(self):
        args = parser.parse_args()
        search_term = args['search_term']
        results = scraper.search_matey(search_term)
        return results

api.add_resource(SearchResults, '/')

if __name__ == '__main__':
    app.run(debug=True)
