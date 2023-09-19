from django.contrib import admin

from coupon.models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ("__str__", "code", "method", "value", "used", "usage_limit")
    filter_horizontal = ("courses", "testseries", "course_category", "testseries_category")
    exclude = ("courses", "testseries")


admin.site.register(Coupon, CouponAdmin)
