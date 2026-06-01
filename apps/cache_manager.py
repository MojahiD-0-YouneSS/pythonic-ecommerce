from django.core.cache import cache
from django.forms.models import model_to_dict


def get_cached_data(
    model_class=None,
    key=None,
    **model_fields,
):
    """Fetches the global context from cache, or hits the DB if missing."""
    CACHE_KEY = key or "probo_context_data"
    TIMEOUT = 60 * 60 * 24  # Cache for 24 hours (or whatever fits your TTL)
    data = cache.get(CACHE_KEY)
    def _hydrate_from_db(cls, **fields):
        """The expensive DB queries that we only want to run once."""
        # Grab the current active system banner
        obj = cls.objects.filter(**fields)
        return model_to_dict(obj)

    if data is None and model_class:
        data = _hydrate_from_db(model_class,**model_fields)
        cache.set(CACHE_KEY, data, TIMEOUT)

    return data

def clear_cache(key=None):
    """Wipes the cache so the next request rebuilds it."""
    CACHE_KEY = key or "probo_context_data"
    cache.delete(CACHE_KEY)

