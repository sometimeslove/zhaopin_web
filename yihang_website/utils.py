from django.contrib.sites.models import Site
from django.core.cache import cache
from hashlib import md5
import logging


logger = logging.getLogger(__name__)


def cache_decorator(expiration=3 * 60):
    def wrapper(func):
        def news(*args, **kwargs):
            try:
                view = args[0]
                key = view.get_cache_key()
            except:
                key = None
                pass
            if not key:
                unique_str = repr((func, args, kwargs))

                m = md5(unique_str.encode('utf-8'))
                key = m.hexdigest()
            value = cache.get(key)
            if value:
                # logger.info('cache_decorator get cache:%s key:%s' % (func.__name__, key))
                if repr(value) == 'default':
                    return None
                else:
                    return value
            else:
                logger.info('cache_decorator set cache:%s key:%s' % (func.__name__, key))
                value = func(*args, **kwargs)
                if not value:
                    cache.set(key, 'default', expiration)
                else:
                    cache.set(key, value, expiration)
                return value

        return news

    return wrapper


@cache_decorator()
def get_current_site():
    site = Site.objects.get_current()
    return site