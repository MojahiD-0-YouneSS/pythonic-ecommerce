# core regestry.py
from dataclasses import dataclass
from django.utils.text import slugify
CORE_SELECTOR_REGISTRY = {}

@dataclass
class SelectorRegestry:
    pass
@dataclass
class CreatorRegestry:
    pass
def register_selector(name=None):
    def wrapper(cls):
        key = name or slugify(cls.__name__).replace("selector", "")
        SelectorRegestry.__setattr__(key,cls())
        return cls
    return wrapper

CORE_CREATOR_REGISTRY = {}

def register_creator(name=None):
    def wrapper(cls):
        key = name or slugify(cls.__name__).replace("creator", "")
        CreatorRegestry.__setattr__(key, cls())
        return cls
    return wrapper
