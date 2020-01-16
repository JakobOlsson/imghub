from os import getenv
import redis

SESSION_KEY = getenv('SESSION_KEY')
SESSION_TYPE = getenv('SESSION_TYPE')
SESSION_REDIS = redis.from_url(getenv('SESSION_REDIS'))
