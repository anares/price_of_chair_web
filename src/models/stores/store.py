import uuid
from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors
import tldextract

class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, numeric_dot=None, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self.numeric_dot = True if numeric_dot is None else numeric_dot
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'url_prefix': self.url_prefix,
            'tag_name': self.tag_name,
            'query': self.query
        }

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {'_id': _id}))

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {'name': store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {'url_prefix': url_prefix}))

    def save_to_db(self):
        Database.update(StoreConstants.COLLECTION, {'_id': self._id}, self.json())

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def find_by_url(cls, url):
        extracted_domain = tldextract.extract(url)
        if url[4] != 's':
            url_prefix = "http://" + extracted_domain.fqdn
        else:
            url_prefix = "https://" + extracted_domain.fqdn
        store = cls.get_by_url_prefix(url_prefix)
        if store is not None:
            return store
        else:
            raise StoreErrors.StoreNotFoundError('The URL Prefix used to find the store didn\'t give us any results')

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]
