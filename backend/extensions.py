"""
extensions.py
-------------
Holds shared extension instances (db, jwt, cors) so models/routes can import
them without circular-importing app.py.

Dependencies: SQLAlchemy, Flask-JWT-Extended, Flask-CORS
"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
