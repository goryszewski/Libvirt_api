from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_marshmallow import Marshmallow

from resources.routers import initialize_routes
from databases.db import db

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

ma = Marshmallow(app)

from databases.db import init_db
from util.env import get_env

init_db(
    {
        "login": get_env("MYSQL_USER"),
        "password": get_env("MYSQL_PASS"),
        "host": get_env("MYSQL_HOST"),
        "db": get_env("MYSQL_DB"),
    }
)

initialize_routes(api)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db["session"].remove()


if __name__ == "__main__":
    app.run(debug=True)
