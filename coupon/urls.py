from django.urls import path

from coupon.views.apis import (
    ValidateCoupon
)

api_urlpatterns = [
    path('coupon/validate-coupon', ValidateCoupon.as_view(), name='validateCoupon'),
]

urlpatterns = api_urlpatterns
