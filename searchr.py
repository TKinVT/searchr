import scraper
import os
from dotenv import load_dotenv
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, Api, reqparse

load_dotenv()

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

parser = reqparse.RequestParser()
parser.add_argument('search_term', required=True)
parser.add_argument('search_type')

# auth stuff
users = {
    "bot": os.getenv("BOT_PASSWORD")
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        if password == users[username]:
            return True
    return False

# posts request with search term, receives results as json
class SearchResults(Resource):
    @auth.login_required
    def post(self):
        args = parser.parse_args()
        search_term = args['search_term']
        search_type = args['search_type']
        results = scraper.search_matey(search_term, search_type)
        return results, 201

# placeholder in order to return something at / for Zappa that has no params
class Dummy(Resource):
    def get(self):
        return {'tk':'loves pk'}


api.add_resource(Dummy, '/')
api.add_resource(SearchResults, '/search')


if __name__ == '__main__':
    app.run(debug=True)
