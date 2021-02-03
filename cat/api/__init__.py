import logging
import sys
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

#Define the WSGI
app = Flask(__name__)

#loading config
app.config.from_object('config')

#define objects
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


#import local
from .controllers import load, BreedsList, BreedApi, TemperamentApi, OriginApi

load()

#register apis
api.add_resource(BreedsList, "/")
api.add_resource(BreedApi, "/breed/<string:name>")
api.add_resource(TemperamentApi, "/temperament/<string:temperament>")
api.add_resource(OriginApi, "/origin/<string:origin>")
