
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['leonbuy-prod.herokuapp.com'] #required if debug is off

DATABASES= {
    'default': dj_database_url.config()
}