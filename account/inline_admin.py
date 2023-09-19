from django.contrib import admin

from account.models import UserTestsetAnswer


class UserTestsetAnswerInLine(admin.StackedInline):
    model = UserTestsetAnswer
    extra = 0
    min_num = 0
    max_num = 0
    can_delete = False
    verbose_name_plural = "Answer sheet"
    classes = ['collapse']
    readonly_fields = ('question', 'answer', 'selected_option', 'status', 'selected_option_status')
    exclude = ('started_at', 'end_at')
