from django_abstract.base.base_exception import CoreException
from django_abstract.exceptions import CreatorException, GenericCreatorException


class CartNotCreatedException(CreatorException):
    """Raised when a cart is not created."""

    def __init__(
        self,
        message,
        creator_name,
        error_code=None,
        original_exception=None,
        context=None,
    ):
        self.message = message or "Cart not created."
        self.creator_name = creator_name
        self.error_code = error_code
        self.original_exception = original_exception
        self.context = context
        super().__init__(self.message, error_code, original_exception, context)


class CartItemNotCreatedException(CreatorException):
    """Raised when a cart item is not created."""

    def __init__(
        self,
        message,
        creator_name,
        error_code=None,
        original_exception=None,
        context=None,
    ):
        self.message = message or "Cart item not created."
        self.creator_name = creator_name
        self.error_code = error_code
        self.original_exception = original_exception
        self.context = context
        super().__init__(self.message, error_code, original_exception, context)
        
class DiscountCodeNotCreatedException(CreatorException):
    """Raised when a discount code is not created."""

    def __init__(
        self,
        message,
        creator_name,
        error_code=None,
        original_exception=None,
        context=None,
    ):
        self.message = message or "Discount code not created."
        self.creator_name = creator_name
        self.error_code = error_code
        self.original_exception = original_exception
        self.context = context
        super().__init__(self.message, error_code, original_exception, context)


class DiscountCodeConnotBeAppliedException(CoreException):
    """Raised when a discount code cannot be applied to the cart."""

    def __init__(self, message, error_code=None, original_exception=None, context=None):
        self.message = message or "Discount code cannot be applied."
        self.error_code = error_code
        self.original_exception = original_exception
        self.context = context
        super().__init__(self.message, error_code, original_exception, context)


class DiscountCodeReachedLimitException(CoreException):
    """Raised when a discount code cannot be applied to the cart."""

    def __init__(self, message, error_code=None, original_exception=None, context=None):
        self.message = (
            message or "Discount code cannot be applied due to breatching limit."
        )
        self.error_code = error_code
        self.original_exception = original_exception
        self.context = context
        super().__init__(self.message, error_code, original_exception, context)
