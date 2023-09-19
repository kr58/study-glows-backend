from django.urls import path

from blog.views.api import (
    BlogList,
    BlogDetail,
    SaveBlog,
    UnsaveBlog,
    SavedBlogView,
)

api_urlpatterns = [
    # blog's api
    path('blogs/<str:category>', BlogList.as_view(), name='blog'),
    path('blog/<int:id>', BlogDetail.as_view(), name='blog_detail'),

    # saved, unsave blog's api
    path('blog/saved', SavedBlogView.as_view(), name='blog_saved'),
    path('blog/<int:id>/save', SaveBlog.as_view(), name='blog_save'),
    path('blog/<int:id>/unsave', UnsaveBlog.as_view(), name='blog_unsave'),
]

urlpatterns = api_urlpatterns
