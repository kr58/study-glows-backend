from rest_framework import serializers

from course.models import CourseSection
from commons.serializer import BaseSerializer
from course.serializers.lecture_serializers import LectureListSerializer, LectureShortSerializer


class CoursesectionListSerializer(BaseSerializer):
    lecture = LectureShortSerializer(read_only=True, many=True)

    class Meta:
        model = CourseSection
        fields = [
            'id',
            'name',
            'lecture',
        ]


class CoursesectionDetailSerializer(BaseSerializer):
    lecturelist = serializers.SerializerMethodField()

    class Meta:
        model = CourseSection
        exclude = [
            'lecture',
            'publish',
            'created_by',
            'created_at',
            'updated_at',
        ]

    def get_lecturelist(self, obj):
        coursesection = obj
        user = self.context.get("user")
        course = self.context.get("course")
        lectures = obj.lecture.filter(publish=True, coursesectionlecture__publish=True)
        return LectureListSerializer(lectures, many=True, context={
            "user": user,
            "course": course,
            "coursesection": coursesection
        }).data
