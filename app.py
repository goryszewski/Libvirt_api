from flask import Flask
from resources.routers import initialize_routes
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

initialize_routes(api)

if __name__ == "__main__":
    app.run(debug=True)