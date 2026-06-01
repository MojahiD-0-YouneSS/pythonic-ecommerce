from django_abstract.base.base_system import BaseSystem
from django_abstract.registry import get_operator

class ClientSystem(BaseSystem):
    """
    Unified entry point for all client operations (auth, profile, settings).
    Orchestrates and delegates calls directly to client operators.
    """
    ALLOWED_OPERATORS=["client_operator"]
    SYSTEM_SLUG  = "client_system"

    def __init__(self, entry=None):
        super().__init__( entry=entry)

    def execute(self, *args, **kwargs):
        """
        Receives an Entry, delegates it to the ClientOperator, and returns
        the processed state back to the view layer.
        """
        # Execute operator and return the resulting data state
        target_service =kwargs.get('target_service') or self.entry.control_entry_data.service_name
        target_method = kwargs.get('target_method')  or self.entry.service_entry_data.service_data.get('method_name')
        if args and target_method and target_service:
            try:

                for operator in args:
                    if operator in self.allowed_operators:
                        success = self.invoke_operator(
                        operator_name=operator,
                        target_service=target_service,
                        target_method=target_method,
                        payload=self.entry.service_entry_data.service_data
                    )
                        if not success:
                            self.entry.errors["system_error"] = (
                                f"{operator} failed! with {target_method , target_service}"
                            )

                            return False, self.entry 
                        self.entry.service_entry_data.service_data.update(
                        success.service_data
                    )
                    else:
                        self.entry.errors['system_error']=f'{operator} not found! available operators are: {self.allowed_operators}'
                        return False, self.entry
                return True, self.entry  

            except Exception as e:
                raise e
                self.entry.service_entry_data.errors['system_error']=str(e)
                return False, self.entry 
        return True, self.entry 
