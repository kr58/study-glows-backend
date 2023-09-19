from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from blog.models import (
    Blog,
    BLOG_CATEGORY,
)


class BlogForm(forms.ModelForm):
    category = forms.ChoiceField(choices=BLOG_CATEGORY)
    content = forms.CharField(widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        models = Blog
        fields = '__all__'
