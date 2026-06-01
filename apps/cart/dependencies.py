# cart dependencies.py
from django_abstract.base.base_dependency import BaseDependency

class CartAppDependency(BaseDependency):
    """
    CartAppDependency is a dataclass that serves as a container for the cart app's dependencies.
    It inherits from BaseDependency, which provides a base structure for defining dependencies in the application.
    """
    app_name: str = "cart"
    description: str = "Cart app dependency"
    version: str = "1.0.0"
