from rest_framework import serializers

from commons.serializer import BaseSerializer
from account.serializers import FAQSerializer
from account.utils import validateUserCourseSubscription

from course.models import Instructor, Category, Feature, Course, Lecture
from course.serializers.course_section_serializers import CoursesectionListSerializer
from course.serializers.lecture_serializers import DemoLectureSerializer


class InstructorSerializer(BaseSerializer):
    class Meta:
        model = Instructor
        fields = ["id", "name", "profile_image", "bio"]


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']


class FeatureSerializer(BaseSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name', 'icon']


class CourseListSerializer(BaseSerializer):
    class Meta:
        model = Course
        exclude = [
            'about',
            'publish',
            'feature',
            'category',
            'faq',
            'instructor',
            'coursesection',
            'created_at',
            'updated_at',
        ]


class CourseDetailSerializer(BaseSerializer):
    faq = FAQSerializer(read_only=True, many=True)
    feature = FeatureSerializer(read_only=True, many=True)
    instructor = InstructorSerializer(read_only=True, many=True)
    coursesection = CoursesectionListSerializer(read_only=True, many=True)
    enrolled = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()
    demo_video = serializers.SerializerMethodField()

    class Meta:
        model = Course
        exclude = [
            'publish',
            'category',
            'created_at',
            'updated_at',
        ]

    def get_enrolled(self, obj):
        user = self.context.get("user")
        course = obj
        if user and user.id and course:
            status, subscription = validateUserCourseSubscription(user, course)
            return status

    def get_saved(self, obj):
        user = self.context.get("user")
        if user and obj.usersavedcourse_set.filter(user=user.id).first():
            return True
        return False

    def get_demo_video(self, obj):
        demo_lectures = Lecture.objects.filter(
            publish=True,
            coursesectionlecture__publish=True,
            coursesectionlecture__is_demo=True,
            coursesectionlecture__coursesection__in=obj.coursesection.all()
        )
        return DemoLectureSerializer(demo_lectures, many=True).data


class SavedCourseListSerializer(BaseSerializer):
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Course
        exclude = [
            'about',
            'publish',
            'feature',
            'faq',
            'instructor',
            'created_at',
            'updated_at',
        ]
