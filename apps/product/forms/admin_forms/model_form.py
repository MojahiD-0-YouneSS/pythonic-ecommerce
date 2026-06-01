from apps.product.models import (
    Product,
    ProductImage,
    ProductVariant,
    Category,
    ReplyModel,
    ReviewModel,
)
from django_abstract.base.base_form import BaseForm

class ProductModelForm(BaseForm):
    class Meta(BaseForm.Meta):
        model =  Product

class ProductImageModelForm(BaseForm):
    class Meta(BaseForm.Meta):
        model =  ProductImage

class ProductVariantModelForm(BaseForm):
    class Meta(BaseForm.Meta):
        model =  ProductVariant

class CategoryModelForm(BaseForm):
    class Meta(BaseForm.Meta):
        model =  Category

class ReplyModelForm(BaseForm):
    class Meta(BaseForm.Meta):
        model =  ReplyModel

class ReviewModelForm(BaseForm):
    class Meta(BaseForm.Meta):
        model =  ReviewModel

