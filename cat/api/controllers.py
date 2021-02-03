import configparser
import requests
import logging
import sys
import json
import time
from datetime import datetime

from elasticsearch import Elasticsearch
from flask_restful import Resource
from api import db, app
from .models import BreedSchema, Breed, BreedImage, BreedImageSchema

cfg = configparser.ConfigParser()
cfg.read('api/config.ini')

try:
    es_host = 'http://case_es:9200'
    logging.info(f'Trying connect to Elastic {es_host}')

    for t in range(5):
        try:
            es = Elasticsearch([es_host])
            logging.info('Sucessfullly connected to Elastic')
        except:
            logging.info('trying connect to Elastic')
            time.sleep(5)

    es.indices.create(index='logs', ignore=400)
    es.indices.create(index='the_cats', ignore=400)
    logging.info('Sucessfullly connect to Elastic')
except:
    logging.error('Houston, we have a problem with Elastic')
    logging.error(sys.exc_info()[0])


def load():
    try:
        logging.info(f"Calling the cat API {cfg['cat']['baseurl'] + cfg['cat']['raca']}")
        querystring = {"attach_breed": "0"}
        headers = {'x-api-key': cfg['cat']['token']}
        response = requests.get(cfg['cat']['baseurl'] + cfg['cat']['raca'], headers=headers, params=querystring)
    except:
        logging.error("Failed to call the cat API")
        logging.error(sys.exc_info()[0])

    try:
        index = {"request": {
            "path": response.url,
            "status_code": response.status_code,
            "header": str(response.headers),
            "duration": response.elapsed.total_seconds(),
            "@timestamp": datetime.now().isoformat()}
        }
        es.index(index="logs", body=index)
    except:
        logging.error("Failed to put logging in elasticsearch")
        logging.error(sys.exc_info()[0])

    try:
        for i in json.loads(response.text):
            if 'image' in i:
                if 'url' in i['image']:
                    image = BreedImage(url_image=i['image']['url'])
                    breed = Breed(name=i['name'], origin=i['origin'],
                                    temperament=i['temperament'], description=i['description'], image=[image])
                    db.session.add(breed)
                    db.session.add(image)
            else:
                breed = Breed(name=i['name'], origin=i['origin'],
                            temperament=i['temperament'], description=i['description'])
                db.session.add(breed)
            db.session.commit()
        logging.info('data persisted successfully')
    except:
        logging.error('houston, we have a problem to persist the data')
        logging.error(sys.exc_info()[0])


class BreedsList(Resource):
    breeds_schema = BreedSchema(many=True)

    def get(self):
        result = Breed.query.all()
        return self.breeds_schema.dump(result)


class BreedApi(Resource):
    breed_schema = BreedSchema()

    def get(self, name):
        result = Breed.query.filter_by(name=name).first_or_404(description='There is no data with {}'.format(name))
        return self.breed_schema.dump(result)


class TemperamentApi(Resource):
    breeds_schema = BreedSchema(many=True)

    def get(self, temperament):
        result = Breed.query.with_entities(Breed.name).filter(Breed.temperament.like('%' + temperament + '%'))
        return self.breeds_schema.dump(result)


class OriginApi(Resource):
    breeds_schema = BreedSchema(many=True)

    def get(self, origin):
        result = Breed.query.with_entities(Breed.name).filter(Breed.origin.like('%' + origin + '%'))
        return self.breeds_schema.dump(result)
