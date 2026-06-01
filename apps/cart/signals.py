# cart signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from apps.cart.models import CartItem
from apps.context_cache import sync

# Whenever a user adds, updates, or deletes an item in their cart,
# we only delete THEIR specific cache key.
@receiver([post_save, post_delete], sender=CartItem)
def invalidate_user_cart_cache(sender, instance, **kwargs):
    # Assuming your Cart model is linked to a session_key or user
    session_key = instance.cart.session

    if session_key:
        cache_key = f"cart_count_{session_key}" # following App_name _ Action _ Session_key pattern

        # Proactively query the accurate count and update the cache instantly.
        new_count = CartItem.objects.filter(cart__session=session_key).count()
        cache.set(cache_key, new_count, timeout=3600)
        sync(cache_key)
