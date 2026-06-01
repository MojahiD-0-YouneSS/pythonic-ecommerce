from django_abstract.base.base_dependency import BaseDependency


class ClientAppDependency(BaseDependency):
    """
    ClientAppDependency is a dataclass that serves as a container for the client app's dependencies.
    It inherits from BaseDependency, which provides a base structure for defining dependencies in the application.
    """
    app_name: str = "client"
    description: str = "Client app dependency"
    version: str = "1.0.0"


def get_client_dependency() -> ClientAppDependency:
    return ClientAppDependency()
