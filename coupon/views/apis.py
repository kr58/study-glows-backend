from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from order.models import Cart
from coupon.models import Coupon

from coupon.utils import validate_coupon_code_with_cart

from commons.responses import (
    RESPONSE_400
)


class ValidateCoupon(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *arg, **kwargs):
        coupon_code = request.data.get('coupon_code')
        cart = Cart.objects.filter(user=request.user, is_checkout=False).first()
        coupon = Coupon.objects.filter(code=coupon_code).first()
        status, coupon_total_discount = validate_coupon_code_with_cart(coupon, cart)
        if status:
            if coupon_total_discount != 0:
                return Response({
                    'message': "success",
                    'coupon_discount': coupon_total_discount,
                    'coupon_id': coupon.id
                }, 200)
        return Response(RESPONSE_400("error"), 400)
