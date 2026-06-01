from apps.global_context import get_global_context
from django.core.cache import cache

def sync(key, fetch_func=None, timeout=86400):
    """
    Ensures the data is in the Context.
    If missing from Context, it pulls from Cache.
    If missing from Cache, it runs fetch_func(), caches it, and puts it in Context.
    """
    context = get_global_context()

    # 1. Try to get it straight from the cache
    data = cache.get(key)

    # 2. If it exists in cache, push it to the UI Context
    if data is not None:
        context.put(key,data)
        return data

    # 3. If cache is empty, but we have a way to fetch it from the DB
    if fetch_func:
        data = fetch_func()
        cache.set(key, data, timeout)
        context.put(key, data)
        return data

    # 4. If it's completely missing and no fetch func, ensure Context is cleared
    context.put(key, None)
    return None

def invalidate(key):
    """
    Used by Django Signals to destroy the data in BOTH places.
    """
    # 1. Delete from distributed cache (Redis/Memcached)
    cache.delete(key)

    # 2. Delete from the in-memory Probo Context
    context = get_global_context()
    context.clear(key)
    # (Use context.remove(key) if your ProboContextProvider has a remove method)
