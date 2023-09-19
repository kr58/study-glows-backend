from num2words import num2words

from django.views import View
from django.shortcuts import render
from django.http import Http404

from order.models import Order


class OrderInvoice(View):
    def get(self, request, *args, **kwargs):
        order_id = request.GET.get('order_id')
        if order_id and order_id != "":
            order = Order.objects.filter(id=int(order_id)).first()
            if order and order.status != 'pending':
                cart = order.cart
                product_details = cart.product_quantity.all()
                subtotal, total_discount, total_tax, total = 0, 0, 0, 0
                for productQ in product_details:
                    productQ.item = productQ.course if productQ.type == "course" else productQ.testseries
                    productQ.cgst = productQ.tax_amount / 2
                    productQ.sgst = productQ.tax_amount / 2

                    subtotal += productQ.amount if productQ.amount else 0
                    total_tax += productQ.tax_amount if productQ.tax_amount else 0
                    total += productQ.total_amount if productQ.total_amount else 0
                    total_discount += productQ.coupon_amount if productQ.coupon_amount else 0

                context = {
                    "order": order,
                    "user": order.user,
                    "total": total,
                    "subtotal": subtotal,
                    "total_tax": total_tax,
                    "total_discount": total_discount,
                    "product_details": product_details,
                    "total_in_words": num2words(total)
                }
                return render(request, 'invoice.html', context)
        raise Http404
