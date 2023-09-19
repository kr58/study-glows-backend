
from multiprocessing import context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from blog.models import (
    Blog,
    BLOG_CATEGORY,
    BlogUser
)

from blog.serializers import (
    BlogSerializer
)

from commons.responses import (
    RESPONSE_404,
    RESPONSE_400
)

class BlogList(APIView):
    paginate_by = 6
    message = 'blog category not found'
    @swagger_auto_schema(tags=["blog"], responses={200: BlogSerializer(many=True), 404: message})
    def get(self, request, format=None, *args, **kwargs):
        category =  kwargs.get('category')
        # print(request.query_params)
        if category and category in [i[0] for i in BLOG_CATEGORY]:
            publish_date = request.query_params.get('publish_date')
            if publish_date and publish_date != "":
                blogs = Blog.objects.filter(publish_status=True, category=category, published_on=publish_date).distinct()
            else:
                blogs = Blog.objects.filter(publish_status=True, category=category).distinct()
            return self.pagination(blogs)
        return Response(RESPONSE_404(self.message), 404)
    
    def pagination(self, blogs):
        page = self.request.GET.get("page")
        paginator = Paginator(blogs, self.paginate_by)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = []
        blogSerializer = BlogSerializer(blogs, many=True, context={"user": self.request.user})
        return_resp = {
            "data": blogSerializer.data,
            "total_page": paginator.num_pages,
            "per_page": paginator.per_page,
            "current_page": int(page) if page else 1
        }
        return Response(return_resp, 200)


class BlogDetail(APIView):
    message = 'Blog does not exits'
    @swagger_auto_schema(tags=["blog"], responses={200: BlogSerializer, 404: message})
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            blog = Blog.objects.filter(id=int(id), publish_status=True).first()
            if blog:
                blogSerializer = BlogSerializer(blog, context={"user": request.user})
                return Response(blogSerializer.data, 200)
        return Response(RESPONSE_404(self.message), 404)


class SavedBlogView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        blogs = Blog.objects.filter(id__in=user.bloguser_set.all().values('blog'))
        return Response(BlogSerializer(blogs, many=True).data, 200)


class SaveBlog(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["blog"], responses={200: "success", 400: "fail"})
    def post(self, request, *args, **kwargs):
        blog_id = kwargs.get('id')
        if blog_id:
            blog = Blog.objects.filter(id=int(blog_id)).first()
            if blog:
                blog_user = BlogUser.objects.update_or_create(
                    user=request.user, blog=blog,
                    defaults={"user": request.user, "blog": blog}
                )
                return Response({
                    "message": "success",
                }, 200)
        return Response({"message": "fail"}, 400)


class UnsaveBlog(APIView):
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["blog"], responses={200: "success", 400: "fail"})
    def post(self, request, *args, **kwargs):
        blog_id = kwargs.get('id')
        if blog_id:
            blog = Blog.objects.filter(id=int(blog_id)).first()
            if blog:
                BlogUser.objects.filter(user=request.user, blog=blog).delete()
                return Response({
                    "message": "success",
                }, 200)
        return Response({"message": "fail"}, 400)
