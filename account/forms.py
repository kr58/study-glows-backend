from django import forms
from django.contrib import auth

from account.models import (
    ContactUs,
    RequestCallBack,
    User,
    UserLectureDoubt
)

from account.constants import (
    CONTACTUS_STATUS,
    LECTURE_DOUBT_STATUS,
    REQUESTCALLBACK_STATUS
)


class CustomUserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=auth.models.Group.objects.all(), required=False)

    class Meta:
        models = User
        fields = '__all__'

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CustomUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ContactusForm(forms.ModelForm):
    choices = (('', '---'), ) + CONTACTUS_STATUS
    status = forms.ChoiceField(choices=choices, required=False)

    class Meta:
        models = ContactUs
        fields = '__all__'


class RequestCallBackForm(forms.ModelForm):
    choices = (('', '---'), ) + REQUESTCALLBACK_STATUS
    status = forms.ChoiceField(choices=choices, required=False)

    class Meta:
        models = RequestCallBack
        fields = '__all__'


class UserLectureDoubtForm(forms.ModelForm):
    choices = (('', '---'), ) + LECTURE_DOUBT_STATUS
    status = forms.ChoiceField(choices=choices, required=False)

    class Meta:
        models = UserLectureDoubt
        fields = '__all__'
