from rest_framework import serializers
from account.models import UserTestset

from commons.serializer import BaseSerializer
from test_series.models import Category, Option, Question, TestSeries, TestSetCategory, Testset, TestsetQuestion
from account.serializers import FAQSerializer, UserSerializer
from account.utils import validateUserTestseriesSubscription


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        exclude = [
            'description',
            'status',
            'created_at',
            'updated_at',
        ]


class FeatureSerializer(BaseSerializer):
    class Meta:
        model = Category
        exclude = [
            'status',
            'created_at',
            'updated_at',
        ]


class Feature2Serializer(BaseSerializer):
    class Meta:
        model = Category
        exclude = [
            'status',
            'created_at',
            'updated_at',
        ]


class TestseriesCategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TestSeriesListSerializer(BaseSerializer):
    class Meta:
        model = TestSeries
        exclude = [
            'about',
            'testset',
            'publish',
            'feature',
            'feature2',
            'category',
            'faq',
            'created_at',
            'updated_at',
        ]


class TestSeriesDetailSerializer(BaseSerializer):
    feature = FeatureSerializer(read_only=True, many=True)
    feature2 = Feature2Serializer(read_only=True, many=True)
    faq = FAQSerializer(read_only=True, many=True)
    enrolled = serializers.SerializerMethodField()

    class Meta:
        model = TestSeries
        exclude = [
            'publish',
            'testset',
            'category',
            'created_at',
            'updated_at',
        ]

    def get_enrolled(self, obj):
        user = self.context.get("user")
        testseries = obj
        if user and user.id and testseries:
            status, subscription = validateUserTestseriesSubscription(user, testseries)
            return status


class TestsetCategroySerializer(BaseSerializer):

    class Meta:
        model = TestSetCategory
        exclude = [
            'publish',
            'created_at',
            'updated_at',
        ]


class TestsetListSerializer(BaseSerializer):
    total = serializers.SerializerMethodField()
    participated_user = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    started = serializers.SerializerMethodField()

    class Meta:
        model = Testset
        exclude = [
            'description',
            'testset_category',
            'questions',
            'publish',
            'order',
            'created_at',
            'updated_at',
        ]

    def get_total(self, obj):
        questions_list = TestsetQuestion.objects.filter(testset=obj, publish=True).values('question__marks')
        questions_list_marks = [i["question__marks"] for i in questions_list]
        return {"questions": len(questions_list_marks), "marks": sum(questions_list_marks)}

    def get_participated_user(self, obj):
        return UserTestset.objects.filter(testset=obj).count()

    def get_started(self, obj):
        user = self.context.get("user")
        testset = obj
        if user and user.id and testset:
            return True if testset.usertestset_set.filter(user=user, completed=False).first() else False
        return False

    def get_completed(self, obj):
        user = self.context.get("user")
        testset = obj
        if user and user.id and testset:
            return True if testset.usertestset_set.filter(user=user, completed=True).first() else False
        return False


class OptionSerializer(BaseSerializer):
    class Meta:
        model = Option
        exclude = [
            'question',
            'correct_status',
            'marks',
            'created_at',
            'updated_at',
        ]


class QuestionDetailSerializer(BaseSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = [
            'max_time',
            'solution',
            'created_at',
            'updated_at',
        ]

    def get_options(self, obj):
        options = obj.option_set.all()
        return OptionSerializer(options, many=True).data


class QuestionListSerializer(BaseSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question')


class TestsetDetailSerializer(BaseSerializer):
    class Meta:
        model = Testset
        exclude = [
            'questions',
            'description',
            'testset_category',
            'publish',
            'order',
            'created_at',
            'updated_at',
        ]


class OnlineTestSerializer(BaseSerializer):
    testseries = TestSeriesListSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    testset = TestsetDetailSerializer(read_only=True)
    test_started_at = serializers.SerializerMethodField()

    class Meta:
        model = UserTestset
        exclude = [
            'subscription',
            'created_at',
            'updated_at',
            'report_generated',
            'report_data'
        ]

    def get_test_started_at(self, obj):
        return obj.started_at
