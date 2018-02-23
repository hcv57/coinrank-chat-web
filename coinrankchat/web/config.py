from os import environ

API_SERVER_HOST = environ.get('API_SERVER_HOST', 'apiserver')
IMAGE_SERVER_URL = environ.get('IMAGE_SERVER_URL ')