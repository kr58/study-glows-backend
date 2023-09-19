from commons.serializer import BaseSerializer

from test_series.serializers import TestSeriesListSerializer
from course.serializers.course_serializers import CourseListSerializer

from order.models import (
    ProductQuantity,
    Cart,
    Order
)

class ProductQuantitySerializer(BaseSerializer):
    course = CourseListSerializer()
    testseries = TestSeriesListSerializer()
    class Meta:
        model = ProductQuantity
        exclude = ['validity', 'created_at', 'updated_at']


class CartSerializer(BaseSerializer):
    product_quantity = ProductQuantitySerializer(many=True)

    class Meta:
        model = Cart
        exclude = ['user', 'checkout_datetime', 'created_at', 'updated_at']


class OrderSerializer(BaseSerializer):
    cart = CartSerializer(read_only=True)

    class Meta:
        model = Order
        exclude = ['user', 'created_at', 'updated_at']
