import razorpay
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from order.models import (
    Cart,
    PRODUCT_TYPE,
    Order,
    Payment,
)
from course.models import Course
from test_series.models import TestSeries
from coupon.models import Coupon

from order.serializers import (
    CartSerializer,
    OrderSerializer
)
from coupon.utils import calculate_coupon_discout_for_product, validate_coupon_code_with_cart
from account.utils import validateUserCourseSubscription, validateUserTestseriesSubscription
from order.utils import after_successful_order_place, get_course_price_detail, get_testseries_price_detail
from commons.responses import RESPONSE_404, RESPONSE_400


class CartView(APIView):
    permission_classes = (IsAuthenticated,)
    empty_message = 'cart is empty'
    course_not_found_message = 'course does not exists'
    testseries_not_found_message = 'testseries does not exists'
    error_message = 'fail'

    def get(self, request, *arg, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user, is_checkout=False).first()
        if cart and cart.product_quantity.count() > 0:
            for productQ in cart.product_quantity.all():
                course = productQ.course
                testseries = productQ.testseries
                price_detail = None
                if productQ.type == "course" and course:
                    price_detail = get_course_price_detail(course)
                if productQ.type == "testseries" and testseries:
                    price_detail = get_testseries_price_detail(testseries)
                if price_detail:
                    productQ.amount = price_detail.get("amount")
                    productQ.tax_amount = price_detail.get("tax_amount")
                    productQ.total_amount = price_detail.get("total_amount")
                    productQ.coupon_amount = 0
                    productQ.save()
                else:
                    productQ.delete()
            return Response(CartSerializer(cart).data, 200)
        return Response(RESPONSE_404(self.empty_message), 404)

    def post(self, request, *arg, **kwargs):
        return self.utils(request, "post")

    def delete(self, request, *arg, **kwargs):
        return self.utils(request, "delete")

    def utils(self, request, method="post"):
        data = request.data
        user = request.user
        if data.get('type') and data.get('type') in [type[0] for type in PRODUCT_TYPE]:
            course_id = data.get('course_id')
            testseries_id = data.get('testseries_id')
            if course_id or testseries_id:
                # check if user has cart. if not create cart for the user
                cart = Cart.objects.filter(user=user, is_checkout=False).first()
                if not cart:
                    cart = Cart.objects.create(user=user)

            if course_id and data.get('type') == "course":
                course = Course.objects.filter(id=int(course_id), publish=True).first()
                if course:
                    # validate course subscription and return if already enrolled
                    status, subscription = validateUserCourseSubscription(user, course)
                    if status:
                        return Response({"message": "already enrolled"}, 400)

                    # update/delete the cart
                    if method == "post":    # update
                        price_detail = get_course_price_detail(course)
                        cart.product_quantity.update_or_create(
                            type=data.get('type'),
                            course=course,
                            amount=price_detail.get("amount"),
                            tax_amount=price_detail.get("tax_amount"),
                            total_amount=price_detail.get("total_amount")
                        )
                        return Response({"message": "success"}, 200)
                    elif method == "delete":   # delete
                        cart.product_quantity.filter(
                            type=data.get('type'),
                            course=course
                        ).delete()
                        return Response({"message": "success"}, 200)
                    return Response({"message": "invalid method"}, 400)
                return Response(RESPONSE_400(self.course_not_found_message), 400)
            if testseries_id and data.get('type') == "testseries":
                testseries = TestSeries.objects.filter(id=int(testseries_id)).first()
                if testseries:
                    # validate course subscription and return if already enrolled
                    status, subscription = validateUserTestseriesSubscription(user, testseries)
                    if status:
                        return Response({"message": "already enrolled"}, 400)

                    # update/delete the cart
                    if method == "post":    # update
                        price_detail = get_testseries_price_detail(testseries)
                        cart.product_quantity.update_or_create(
                            type=data.get('type'),
                            testseries=testseries,
                            amount=price_detail.get("amount"),
                            tax_amount=price_detail.get("tax_amount"),
                            total_amount=price_detail.get("total_amount")
                        )
                        return Response({"message": "success"}, 200)
                    elif method == "delete":   # delete
                        cart.product_quantity.filter(
                            type=data.get('type'),
                            testseries=testseries
                        ).delete()
                        return Response({"message": "success"}, 200)
                    return Response({"message": "invalid method"}, 200)
                return Response(RESPONSE_400(self.testseries_not_found_message), 400)
            return Response({"message": "invalid type or id"}, 400)
        return Response(RESPONSE_400(self.error_message), 400)


class CheckoutView(APIView):
    permission_classes = (IsAuthenticated,)
    cart_not_found_message = 'cart not found'
    error_message = 'fail'

    def post(self, request, *arg, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user, is_checkout=False).first()
        input_total = request.data.get('total')

        # check if cart exits and check if user's cart
        if cart and cart.user and cart.user == user:
            total_cost = cart.get_cart_total()
            if total_cost != input_total:
                return Response(RESPONSE_400(self.error_message), 400)
            order = Order.objects.update_or_create(
                user=user,
                cart=cart,
                status='pending',
                total=total_cost,
            )
            return Response(OrderSerializer(order).data, 200)
        return Response(RESPONSE_400(self.cart_not_found_message), 400)


class PlaceOrderView(APIView):
    permission_classes = (IsAuthenticated,)
    already_paid_message = "already paids"
    error_message_for_razorpay = "error with razorpay"
    error_message_for_total = "total incorrect"
    order_not_found = "order not found"
    error = "error"

    def post(self, request, *arg, **kwargs):
        user = request.user
        coupon_code = request.data.get('coupon_code')
        total = request.data.get('total')
        cart = Cart.objects.filter(user=user, is_checkout=False).first()
        if cart and total:
            order = Order.objects.filter(cart=cart).first()
            if order:
                # TODO: Billing address

                coupon_applied, coupon = False, None
                if coupon_code and coupon_code != "":
                    coupon = Coupon.objects.filter(code=coupon_code).first()
                    status, coupon_total_discount = validate_coupon_code_with_cart(coupon, cart)
                    if status:
                        coupon_applied = True

                if coupon_applied and coupon:
                    order.coupon = coupon
                    cart.update_cart_for_coupon(coupon)
                else:
                    order.coupon = None
                    cart.update_cart_for_coupon(None, "remove")

                order_total = cart.get_cart_total()
                if order_total > 0 and float(order_total) == float(total):
                    order.total = order_total
                    order.save()

                    client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
                    amount = float('%.2f' % order.total)
                    amount *= 100
                    resp = client.order.create(dict(
                        amount=amount,
                        currency='INR',
                        receipt=str(order.id)
                    ))

                    if resp['status'] == "created":
                        payment = Payment.objects.filter(order=order.id).first()
                        if payment:
                            if payment.status:  # if payment is done
                                return Response(RESPONSE_400(self.already_paid_message), 400)
                            else:
                                payment.method = "razorpay"
                                payment.razorpay = resp['id']
                                payment.save()
                        else:
                            payment = Payment.objects.create(
                                order=order,
                                method="razorpay",
                                razorpay=resp['id']
                            )
                        return Response({"message": "success", "amount": order.total, "razorpay_order_id": resp['id']}, 200)
                    return Response(RESPONSE_400(self.error_message_for_razorpay), 400)
                return Response(RESPONSE_400(self.error_message_for_total), 400)
            return Response(RESPONSE_400(self.order_not_found), 400)
        return Response(RESPONSE_400(self.error), 400)


class SuccessPaymentView(APIView):
    payment_not_capture = "payment not captured"
    already_paid_message = "already paids"
    error = "error"

    def post(self, request, *arg, **kwargs):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
        razorpayOrderId = request.data.get('razorpay_order_id')
        razorpayPaymentId = request.data.get('razorpay_payment_id')
        if razorpayOrderId and razorpayPaymentId:
            razorpayPayment = client.order.payments(razorpayOrderId)

            if razorpayPayment['items'][0]['status'] == 'captured':
                # Update the payment status
                payment = Payment.objects.filter(razorpay=razorpayOrderId).first()

                if payment and not payment.status:
                    payment.transation_id = razorpayPaymentId
                    payment.status = True
                    payment.save()

                    # after successful payment
                    after_successful_order_place(payment, 'paid')
                    return Response({"message": "success", "razorpay_order_id": razorpayOrderId, "razorpay_payment_id": razorpayPaymentId})
                return Response(RESPONSE_400(self.already_paid_message), 400)
            return Response(RESPONSE_400(self.payment_not_capture), 400)
        return Response(RESPONSE_400(self.error), 400)
