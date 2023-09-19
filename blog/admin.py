from django.contrib import admin
from blog.forms import BlogForm

from blog.models import Blog, BlogUser

class BlogAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category', 'title', 'publish_status', 'posted_by')
    list_filter = ('publish_status', 'category')
    form = BlogForm


class BlogUserAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user')


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogUser, BlogUserAdmin)
