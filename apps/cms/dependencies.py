# cms dependencies.py
from django_abstract.base.base_dependency import BaseDependency


class CmsAppDependency(BaseDependency):
    app_name = 'cms'

def get_cms_app_dependency():
    return CmsAppDependency()