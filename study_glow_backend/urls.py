from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="QSI"
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # api specification
    path('api-specification', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # account
    path('', include('account.urls')),
    
    # blog
    path('', include('blog.urls')),

    # blog
    path('', include('course.urls')),

    # testseries
    path('', include('test_series.urls')),

    # order
    path('', include('order.urls')),

    # coupon
    path('', include('coupon.urls')),

    # ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

admin.site.site_header = 'Study Glow Admin Console'
admin.site.site_title = 'Study Glow Admin'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
