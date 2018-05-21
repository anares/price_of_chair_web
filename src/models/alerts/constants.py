import os

URL = os.environ.get('MAILGUN_URL')
API_KEY = os.environ.get('MAILGUN_API_KEY')
FROM = os.environ.get('MAILGUN_FROM')
MINUTES_FOR_UPDATE = 10
COLLECTION = 'alerts'
