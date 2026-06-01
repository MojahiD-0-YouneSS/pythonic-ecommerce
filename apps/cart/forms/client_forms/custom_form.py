from django import forms
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class QuantityUpdateForm(forms.Form):
    """
    A robust Django Form for updating cart item quantities.
    Validates limits and enforces clean integer inputs.
    """

    quantity = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(
            attrs={
                "class": "form-control text-center fw-bold m-2",
                "min": "1",
                "style": "max-width: 80px;",
            }
        ),
        initial=1,
        label="Quantity",
    )

    def __init__(self, *args, max_stock=None, **kwargs):
        """
        Allows passing 'max_stock' dynamically from your CartItemModelService
        to restrict the upper bound of the input both in HTML5 and the Python clean cycle.
        """
        super().__init__(*args, **kwargs)
        self.max_stock = max_stock

        if max_stock is not None:
            # Inject HTML5 'max' attribute for client-side validation
            self.fields["quantity"].widget.attrs["max"] = str(max_stock)

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")

        # Enforce inventory safety check at the form validation layer
        if self.max_stock is not None and quantity > self.max_stock:
            raise ValidationError(
                f"Cannot update quantity. Only {self.max_stock} units are left in stock."
            )
        return quantity
