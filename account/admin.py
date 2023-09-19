from django.contrib import admin
from account.inline_admin import UserTestsetAnswerInLine

from account.models import (
    Subscription,
    User,
    ContactUs,
    RequestCallBack,
    FAQ,
    UserCourseProgress,
    UserLectureDoubt,
    UserTestset,
    UserTestsetAnswer,
)

from account.forms import (
    ContactusForm,
    CustomUserForm,
    RequestCallBackForm,
    UserLectureDoubtForm
)


class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'username', 'email', 'phone', 'active', 'email_verified', 'phone_verified', 'staff', 'admin', 'created_at', 'id')
    list_filter = ('active', 'staff', 'admin', 'email_verified', 'phone_verified')
    search_fields = ('email', 'phone', )
    exclude = ('user_permissions', 'is_superuser')
    fieldsets = (
        (None, {
            'fields': (
                'password', 'username', 'email', 'phone',
                ('active', 'email_verified', 'phone_verified'),
                'last_login',
                ('address', 'country', 'city', 'state')

            )
        }),
        ('User Permission Management', {
            'classes': ('collapse',),
            'fields': (
                'groups',
                ('staff', 'admin')
            ),
        })
    )
    form = CustomUserForm


class FAQAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'type', 'publish', 'question')
    list_filter = ('publish', 'type')
    search_fields = ('question', 'type')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'type', 'order_ref', 'expire_status')
    list_filter = ('expire_status', 'type')
    search_fields = ('id',)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'email', 'phone', 'status')
    list_filter = ('status',)
    form = ContactusForm


class RequestCallBackAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'email', 'phone', 'status')
    list_filter = ('status',)
    form = RequestCallBackForm


class UserCourseProgressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'course', 'coursesection', 'lecture', 'status', 'completed_on')
    list_filter = ('status',)


class UserTestsetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'testset', 'testseries', 'completed', 'started_at', 'end_at')
    list_filter = ('completed',)
    autocomplete_fields = ('user', 'testset', 'testseries', 'subscription')
    readonly_fields = ('user', 'testset', 'testseries', 'completed', 'started_at', 'end_at', 'subscription')
    exclude = ('report_data',)
    inlines = [
        UserTestsetAnswerInLine
    ]

    def has_add_permission(self, request, obj=None):
        return False


class UserTestsetAnswerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_testset')

    def has_add_permission(self, request, obj=None):
        return False


class UserLectureDoubtAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'user', 'course', 'lecture', 'subject')
    list_filter = ('status',)
    form = UserLectureDoubtForm


admin.site.register(FAQ, FAQAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(UserTestset, UserTestsetAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(RequestCallBack, RequestCallBackAdmin)
admin.site.register(UserLectureDoubt, UserLectureDoubtAdmin)
admin.site.register(UserTestsetAnswer, UserTestsetAnswerAdmin)
admin.site.register(UserCourseProgress, UserCourseProgressAdmin)
