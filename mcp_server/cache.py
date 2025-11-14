from cachetools import TTLCache

_cache = TTLCache(maxsize=1000, ttl=5)


def get_cached(key):
    return _cache.get(key)


def set_cached(key, value):
    _cache[key] = value
