from rest_framework import serializers
from account.serializers import UserSerializer
from commons.serializer import BaseSerializer

from blog.models import Blog


class BlogSerializer(BaseSerializer):
    posted_by = UserSerializer(read_only=True)
    saved = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        exclude = [
            'publish_status',
            'block_status',
            'created_at',
            'updated_at'
        ]
    
    def get_saved(self, obj):
        user = self.context.get("user")
        if user and obj.bloguser_set.filter(user=user.id).first():
            return True
        return False
