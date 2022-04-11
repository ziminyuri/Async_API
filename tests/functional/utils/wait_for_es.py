import logging
import os

import backoff
from elasticsearch import Elasticsearch

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9210))

es = Elasticsearch([f'{ELASTIC_HOST}:{ELASTIC_PORT}'], verify_certs=True)
logger = logging.getLogger()


@backoff.on_exception(backoff.expo, ConnectionError, max_tries=20)
def check_es():
    if not es.ping():
        logger.info('ES not connected, retry...')
        raise ConnectionError
    else:
        logger.info('ES connected.')


if __name__ == '__main__':
    check_es()
