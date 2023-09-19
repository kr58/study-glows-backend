from commons.serializer import BaseSerializer
from rest_framework import serializers

from account.models import (
    FAQ,
    Subscription,
    User,
    ContactUs,
    RequestCallBack,
    UserLectureDoubt,
    UserTestsetAnswer,
)
from test_series.models import TestsetQuestion


class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone',
            'full_name',
            'profile_image',
            'address',
            'state',
            'city',
            'country'
        )
        extra_kwargs = {
            'email': {'required': False}
        }

    def validate(self, attrs):
        # if attrs['password'] != attrs['password2']:
        #     raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def update(self, obj, validated_data):
        obj.full_name = validated_data.get('full_name', obj.full_name)
        obj.email = validated_data.get('email', obj.email)
        obj.profile_image = validated_data.get('profile_image', obj.profile_image)
        obj.address = validated_data.get('address', obj.full_name)
        obj.state = validated_data.get('state', obj.email)
        obj.city = validated_data.get('city', obj.profile_image)
        obj.country = validated_data.get('country', obj.profile_image)
        obj.save()
        return obj


class ContactUsSerializer(BaseSerializer):
    class Meta:
        model = ContactUs
        exclude = ['status']
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
            'message': {'required': True},
        }


class RequestCallBackSerializer(BaseSerializer):
    class Meta:
        model = RequestCallBack
        exclude = ['status']
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
        }


class FAQSerializer(BaseSerializer):
    class Meta:
        model = FAQ
        exclude = ['publish', 'created_at', 'updated_at']


class SubscriptionSerializer(BaseSerializer):
    from course.serializers.course_serializers import CourseListSerializer
    from test_series.serializers import TestSeriesListSerializer

    course = CourseListSerializer(read_only=True)
    testseries = TestSeriesListSerializer(read_only=True)

    class Meta:
        model = Subscription
        exclude = ['user', 'order_ref', 'created_at', 'updated_at']


class UserTestsetAnswerListSerializer(BaseSerializer):
    section = serializers.SerializerMethodField()

    class Meta:
        model = UserTestsetAnswer
        exclude = [
            'comment',
            'question',
            'created_at',
            'updated_at',
            'check_status',
            'user_testset',
            'marks_awarded',
            'selected_option_status',
        ]

    def get_section(self, obj):
        testsetquestion = TestsetQuestion.objects.filter(
            testset=obj.user_testset.testset,
            question=obj.question
        ).first()
        if testsetquestion and testsetquestion.section:
            return testsetquestion.section
        return "default"


class UserTestsetAnswerDetailSerializer(BaseSerializer):
    from test_series.serializers import QuestionDetailSerializer

    question = QuestionDetailSerializer(read_only=True)

    class Meta:
        model = UserTestsetAnswer
        exclude = [
            'comment',
            'created_at',
            'updated_at',
            'check_status',
            'user_testset',
            'marks_awarded',
            'selected_option_status',
        ]


class AskDoubtSerializer(BaseSerializer):
    class Meta:
        model = UserLectureDoubt
        exclude = ['status', 'reply', 'user']
        extra_kwargs = {
            'user': {'required': True},
            'query': {'required': True},
            'course': {'required': True},
            'subject': {'required': True},
            'lecture': {'required': True},
            'coursesection': {'required': True},
        }

    def create(self, validated_data):
        doubt = UserLectureDoubt(**validated_data)
        doubt.user = self.context['request'].user
        doubt.save()
        return doubt
