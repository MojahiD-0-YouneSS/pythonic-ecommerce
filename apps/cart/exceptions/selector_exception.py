from django_abstract.base.base_exception import CoreException
from django_abstract.exceptions import SelectorException, GenericSelectorException

class CartNotFoundException(SelectorException):
    """Raised when a cart is not found."""
    def __init__(self,selector_name, message=None, error_code=None, original_exception=None, context=None):
        self.message = message or f"Cart not found using {{self.selector_name}} selector."
        self.selector_name = selector_name
        self.error_code = error_code or "500"
        self.original_exception = original_exception
        self.context = context
        super().__init__(self.message, error_code, original_exception, context)

class CartItemNotFoundException(SelectorException):
    """Raised when a cart item is not found."""
    def __init__(self,  selector_name,message=None, error_code=None, original_exception=None, context=None):
        self.message = message or f"Cart item not found using {{self.selector_name}} selector."
        self.selector_name = selector_name
        self.error_code = error_code or "500"
        self.original_exception = original_exception
        self.context = context
        super().__init__(self.message, error_code, original_exception, context)

class DiscountCodeNotFoundException(SelectorException):
    """Raised when a discount code is not found."""
    def __init__(self,  selector_name,message=None, error_code=None, original_exception=None, context=None):
        self.message = message or f"Discount code not found using {{self.selector_name}} selector."
        self.selector_name = selector_name
        self.error_code = error_code or "500"
        self.original_exception = original_exception
        self.context = context
        super().__init__(self.message, error_code, original_exception, context)

class DiscountCodeConnotBeAppliedException(CoreException):
    """Raised when a discount code cannot be applied to the cart."""
    def __init__(self, message, error_code=None, original_exception=None, context=None):
        self.message = message or "Discount code cannot be applied."
        self.error_code = error_code or "500"
        self.original_exception = original_exception
        self.context = context
        super().__init__(self.message, error_code, original_exception, context)
        
class DiscountCodeReachedLimitException(CoreException):
    """Raised when a discount code cannot be applied to the cart."""
    def __init__(self, message, error_code=None, original_exception=None, context=None):
        self.message = message or "Discount code cannot be applied due to breatching limit."
        self.error_code = error_code or "500"
        self.original_exception = original_exception
        self.context = context
        super().__init__(self.message, error_code, original_exception, context)