from django.db import models
from django.utils.text import slugify

from commons.models import TimeStampedModel
from account.models import User

BLOG_CATEGORY = (
    ('current_affair', 'current_affair'),
    ('editorial', 'editorial'),
    ('job', 'job'),
    ('result', 'result'),
)

BLOG_LANGUAGE = (
    ('english', 'english'),
    ('hindi', 'hindi'),
)


class Blog(TimeStampedModel):
    category = models.CharField(max_length=256, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    tags = models.CharField(max_length=2048, blank=True, null=True)
    short_content = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    alt = models.CharField(max_length=1024, blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True, upload_to='blog/%Y%m%d')
    published_on = models.DateTimeField(null=True, blank=True)
    publish_status = models.BooleanField(default=False)
    block_status = models.BooleanField(default=False)
    language = models.CharField(max_length=512, blank=True, null=True)
    views = models.PositiveBigIntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=1024, blank=True, null=True)
    posted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)


class BlogUser(TimeStampedModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.blog and self.user:
            return f"blog_user {str(self.blog.pk)}, {str(self.user.pk)}"
        return str(self.pk)
