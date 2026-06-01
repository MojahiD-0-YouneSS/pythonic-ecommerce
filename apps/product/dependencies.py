# product dependencies.py


from django_abstract.base import BaseDependency

class ProductAppDependecy(BaseDependency):
    app_name="product"

def get_product_app_dependency() -> ProductAppDependecy:
    return ProductAppDependecy()
