from account.models import Subscription
from django.utils import timezone
from commons.mail import SendEmail


def get_course_price_detail(course):
    tax_rate = 18
    tax_amount = (course.price*tax_rate)/100
    return {
        "amount": course.price - tax_amount,
        "tax_amount": tax_amount,
        "total_amount":  course.price
    }


def get_testseries_price_detail(tesseries):
    tax_rate = 18
    tax_amount = (tesseries.price*tax_rate)/100
    return {
        "amount": tesseries.price - tax_amount,
        "tax_amount": tax_amount,
        "total_amount":  tesseries.price
    }


def after_successful_order_place(payment, status="pending"):
    order = payment.order
    cart = order.cart
    user = order.user

    if status == 'paid':
        # make the cart checkout
        cart.is_checkout = True
        cart.checkout_datetime = timezone.now()
        cart.save()

        # update the order placed time
        order.order_placed = timezone.now()
        order.status = status
        order.save()

        send_order_confirmation_email(order, user)

        # make the user subscribe to the order's cart items
        for cart_item in cart.product_quantity.all():
            if cart_item.type == 'course':
                # todo add validity & expired on
                Subscription.objects.update_or_create(
                    type=cart_item.type,
                    user=user,
                    course=cart_item.course,
                    order_ref=order,
                    defaults={
                        'type': cart_item.type,
                        'user': user,
                        'course': cart_item.course,
                        'order_ref': order,
                    },
                )
            if cart_item.type == 'testseries':
                # TODO:: add validity & expired on
                Subscription.objects.update_or_create(
                    type=cart_item.type,
                    user=user,
                    testseries=cart_item.testseries,
                    order_ref=order,
                    defaults={
                        'type': cart_item.type,
                        'user': user,
                        'testseries': cart_item.testseries,
                        'order_ref': order,
                    },
                )


def send_order_confirmation_email(order, user):
    if order and order.status != 'pending':
        cart = order.cart
        product_details = cart.product_quantity.all()
        subtotal, total_discount, total_tax, total = 0, 0, 0, 0
        for productQ in product_details:
            productQ.item = productQ.course if productQ.type == "course" else productQ.testseries

            subtotal += productQ.amount if productQ.amount else 0
            total_tax += productQ.tax_amount if productQ.tax_amount else 0
            total += productQ.total_amount if productQ.total_amount else 0
            total_discount += productQ.coupon_amount if productQ.coupon_amount else 0

        data = {
            "order": order,
            "user": order.user,
            "total": total,
            "subtotal": subtotal,
            "total_tax": total_tax,
            "total_discount": total_discount,
            "product_details": product_details,
        }
        if user.email != "":
            sendEmail = SendEmail('email/order_confirmed.html', data, 'Study Glow: Order Confirmed')
            sendEmail.send((user.email,))
