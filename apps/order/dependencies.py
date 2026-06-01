from django_abstract.base import BaseDependency

class OrderAppDependency(BaseDependency):
    app_name='order'
    description='order app central crud controler'

def get_order_dependency():
    return OrderAppDependency()
