from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from order.models import (
    ProductQuantity,
    Cart,
    Order,
    Payment,
)

from order.inline_admin import (
    ProductQuantityInLine
)

from order.forms import (
    OrderForm
)


class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_checkout', 'checkout_datetime',)
    list_filter = ('is_checkout', )
    exclude = ('product_quantity', )
    inlines = [
        ProductQuantityInLine,
    ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'status', 'total', 'Invoice', 'order_placed')
    list_filter = ('status',)
    exclude = ('billing_detail',)
    form = OrderForm

    readonly_fields = (
        'Payment', 'Invoice',
        'Cart', 'User',
        'total', 'created_at', 'updated_at', 'order_placed',
    )
    fieldsets = (
        (None, {
            'fields': (
                'Cart',
                'User',
                'status',
                'total',
                'Payment',
                'Invoice',
                'order_placed'
            )
        }),
        ('Advanced Detail', {
            'classes': ('collapse',),
            'fields': (
                'coupon',
                'created_at', 'updated_at',
            ),
        }),
    )

    def Invoice(self, obj):
        if obj.status != "pending":
            return format_html('<a href="{}"  target="_blank" rel="noopener noreferrer">Invoice</a>', reverse('order_invoice') + '?order_id=' + str(obj.id))
        else:
            return format_html('<a href="">-</a>')

    def Payment(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.payment._meta.app_label, obj.payment._meta.model_name), args=[obj.payment.id])
        return format_html('<a href="{}">Payment Detail</a>', url, obj.payment.id)

    def Cart(self, obj):
        cart = obj.cart
        url = reverse('admin:%s_%s_change' % (cart._meta.app_label, cart._meta.model_name), args=[cart.id])
        html = f'{cart}<ol>'
        for productQ in cart.product_quantity.all():
            html += f'<li>{productQ}</li>'
        html += '</ol>'
        html += f'<a style="padding:5px" href="{url}"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>'
        return format_html(html)

    def User(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label, obj.user._meta.model_name), args=[obj.user.id])
        return format_html('{}<a style="padding:5px" href="{}"><img src="/static/admin/img/icon-changelink.svg" alt="Change"></a>', obj.user, url)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'status', 'method')
    list_filter = ('status',)


class ProductQuantityAdmin(admin.ModelAdmin):
    search_fields = ('course', 'testseries', 'type')
    autocomplete_fields = ('course', 'testseries')
    exclude = ('extra',)


admin.site.register(ProductQuantity, ProductQuantityAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
