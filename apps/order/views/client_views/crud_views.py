from apps.order.forms.client_forms.model_form import BillingAddressModelForm
from django.views import View
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from apps.order.dependencies import OrderAppDependency
from apps.global_context import get_global_context
from django.forms.models import model_to_dict

from ui.components.client.profile import (
    OrderHistorySection,
    AddressBookSection,
)
from django.forms.models import model_to_dict



