from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from database import get_conn_str
from views import create_api

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = get_conn_str()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = create_api()
    api.init_app(app)
    return app


if __name__ == "__main__":
    print(f"Creating a db connection @ {get_conn_str()}")
    api_app = create_app()
    api_app.run(debug=True)
