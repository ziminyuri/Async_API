import os
import time

from elasticsearch import Elasticsearch

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9210))

es = Elasticsearch([f'{ELASTIC_HOST}:{ELASTIC_PORT}'], verify_certs=True)

while not es.ping():
    print('ES not connected, retry in 10 seconds...')
    time.sleep(10)
else:
    print('ES connected.')
