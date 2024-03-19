from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from resources.routers import initialize_routes
from databases.db import db


app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')

CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

from databases.db import init_db
from databases.mongo import init_mongo
from util.env import get_env

init_db(
    {
        "login": get_env("MYSQL_USER"),
        "password": get_env("MYSQL_PASS"),
        "host": get_env("MYSQL_HOST"),
        "db": get_env("MYSQL_DB"),
    }
)

init_mongo(
    {
        "login": get_env("MONGO_USER"),
        "password": get_env("MONGO_PASS"),
        "host": get_env("MONGO_HOST"),
        "db": get_env("MONGO_DB"),
    }
)


initialize_routes(api)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db["session"].remove()


if __name__ == "__main__":
    app.run(debug=True)
