#!/usr/bin/python3
'''A LFU Caching module'''
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    '''A last-in-first-out cache'''
    def __init__(self):
        super().__init__()
        self.key_rank = {}

    def get_rank(self, order):
        '''Gets the lowest or highest ranked key'''
        r = sorted(self.key_rank.items(), key=lambda x: x[1], reverse=order)
        return r[0][0]

    def put(self, key, item):
        '''Puts item in the cache'''
        d = self.cache_data
        if key is not None and item is not None:
            if len(d) < BaseCaching.MAX_ITEMS or key in d:
                d.update({key: item})
                if key not in self.key_rank:
                    self.key_rank.update({key: 0})
                else:
                    self.key_rank[key] += 1
            else:
                rank = self.get_rank(False)
                d.pop(rank)
                self.key_rank.pop(rank)
                d.update({key: item})
                self.key_rank.update({key: 0})
                print('DISCARD:', rank)

    def get(self, key):
        '''Gets item from cache'''
        try:
            if key in self.cache_data:
                self.key_rank[key] += 1
            return self.cache_data[key]
        except Exception:
            return None
