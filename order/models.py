import json
from django.db import models

from commons.models import TimeStampedModel
from account.models import User
from coupon.models import Coupon
from coupon.utils import calculate_coupon_discout_for_product
from course.models import Course
from commons.constants import PRODUCT_TYPE
from test_series.models import TestSeries


ORDER_STATUS = (
    ('pending', 'pending'),
    ('confirmed', 'confirmed'),
    ('paid', 'paid'),
    ('cancelled', 'cancelled'),
    # ('refund', 'refund'),
)


def test_and_get_key_from_dict(dictionary, key):
    return dictionary[key] if dictionary.get(key) and dictionary[key] != "" else None


class ProductQuantity(TimeStampedModel):
    type = models.CharField(max_length=216, blank=True, null=True, choices=PRODUCT_TYPE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    testseries = models.ForeignKey(TestSeries, on_delete=models.CASCADE, blank=True, null=True)
    validity = models.PositiveIntegerField(default=0, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    tax_amount = models.FloatField(blank=True, null=True)
    coupon_amount = models.FloatField(blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)
    extra = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.type == "course":
            return str(self.course.title) if self.course else f'PQ #{self.pk}'
        if self.type == "testseries":
            return str(self.testseries.title) if self.testseries else f'PQ #{self.pk}'
        return f'PQ #{self.pk}'

    def load_extra_json_data(self):
        extra = json.loads(self.extra) if self.extra else {}
        self.tax_rate = test_and_get_key_from_dict(extra, "tax_rate")
        self.tax_cgst = test_and_get_key_from_dict(extra, "tax_cgst")
        self.tax_sgst = test_and_get_key_from_dict(extra, "tax_sgst")
        self.tax_igst = test_and_get_key_from_dict(extra, "tax_igst")

    def dump_extra_data(self, tax_rate=18, tax_cgst=9, tax_sgst=9, tax_igst=None):
        data = {
            "tax_rate": tax_rate,
            "tax_cgst": tax_cgst,
            "tax_sgst": tax_sgst,
            "tax_igst": tax_igst
        }
        return json.dumps(data)


class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_checkout = models.BooleanField(default=False)
    checkout_datetime = models.DateTimeField(blank=True, null=True)
    product_quantity = models.ManyToManyField(ProductQuantity, blank=True)

    def __str__(self):
        return f'cart #{str(self.pk)}'

    def get_cart_total(self):
        _total = 0
        for productQ in self.product_quantity.all():
            _total += productQ.total_amount
        return _total

    def update_cart_for_coupon(self, coupon=None, action="add"):  # action: "add" | "remove"
        if action == "add" and coupon:
            for productQ in self.product_quantity.all():
                coupon_amount = calculate_coupon_discout_for_product(productQ, coupon)
                productQ.coupon_amount = coupon_amount
                productQ.total_amount = productQ.amount + productQ.tax_amount - coupon_amount
                productQ.save()
        if action == "remove":
            for productQ in self.product_quantity.all():
                if productQ.coupon_amount > 0:
                    coupon_amount = 0
                    productQ.coupon_amount = coupon_amount
                    productQ.total_amount = productQ.amount + productQ.tax_amount - coupon_amount
                    productQ.save()


class Order(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, blank=True, null=True)
    total = models.FloatField(default=0, blank=True, null=True)
    status = models.CharField(max_length=216, blank=True, null=True)
    order_placed = models.DateTimeField(blank=True, null=True)
    billing_detail = models.TextField(blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f'order#{str(self.pk)}'

    class Meta:
        ordering = ('-updated_at',)


class Payment(TimeStampedModel):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    method = models.CharField(max_length=216, blank=True, null=True)
    razorpay = models.CharField(max_length=512, blank=True, null=True)
    transation_id = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return f'payment#{str(self.pk)}'

    class Meta:
        ordering = ('-updated_at',)
