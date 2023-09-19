from django.contrib import admin

from order.models import Cart


class ProductQuantityInLine(admin.TabularInline):
    model = Cart.product_quantity.through
    autocomplete_fields = ('productquantity',)
    extra = 0
    verbose_name_plural = "Product Quantity"