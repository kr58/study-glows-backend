from django.urls import path
from .views.admin import OrderInvoice

from order.views.api import (
    CartView,
    CheckoutView,
    PlaceOrderView,
    SuccessPaymentView,
)

api_urlpatterns = [
    # cart's api
    path('cart', CartView.as_view(), name='cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('checkout/place_order', PlaceOrderView.as_view(), name='place_order'),

    # # order's api
    # path('order/place-order', OrderView.as_view(), name='order_place'),
    # path('order/process-payment', ProccessPaymentView.as_view(), name='proccess-payment'),

    # payment
    path('order/success-payment', SuccessPaymentView.as_view(), name='success_payment'),

    path('order/invoice', OrderInvoice.as_view(), name='order_invoice')
]

urlpatterns = api_urlpatterns
