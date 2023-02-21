#!/usr/bin/python3
'''Base Cache class module'''
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    '''Basic Cache class'''
    def __init__(self):
        super().__init__()

    def put(self, key, item):
        '''Put item in cache'''
        if key is not None and item is not None:
            self.cache_data.update({key: item})

    def get(self, key):
        '''Gets item from cache'''
        try:
            return self.cache_data[key]
        except Exception:
            return None
