from rest_framework import serializers

from account.models import UserCourseProgress
from commons.serializer import BaseSerializer

from course.models import Lecture, Resources, Video, VideoV2, Document, RefImage, SubjectiveTest, Chapter


class ResourseSerializer(BaseSerializer):
    class Meta:
        model = Resources
        exclude = [
            'extra',
            'publish',
            'created_at',
            'updated_at',
        ]


class VideoSerializer(BaseSerializer):
    videoType = serializers.SerializerMethodField()
    videoURL = serializers.SerializerMethodField()

    class Meta:
        model = Video
        exclude = [
            'video',
            'length',
            'publish',
            'hls_status',
            'hls_video',
            'hls_updated_at',
            'created_at',
            'updated_at',
        ]

    def get_videoType(self, obj):
        if obj.hls_status and obj.hls_video:
            return "hls"
        elif obj.video:
            return "mp4"
        else:
            return ""

    def get_videoURL(self, obj):
        if obj.hls_status and obj.hls_video:
            return obj.hls_video
        elif obj.video:
            return obj.video.url
        else:
            return ""


class LectureListSerializer(BaseSerializer):
    complete_status = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = ['id', 'name', 'complete_status']

    def get_complete_status(self, obj):
        user = self.context.get("user")
        course = self.context.get("course")
        coursesection = self.context.get("coursesection")
        if user and course and coursesection:
            user_course_progress = UserCourseProgress.objects.filter(
                user=user,
                course=course,
                coursesection=coursesection,
                lecture=obj.id
            ).first()
        return user_course_progress.status if user_course_progress else False


class LectureSerializer(BaseSerializer):
    resourse = ResourseSerializer(read_only=True, many=True)
    video = VideoSerializer(read_only=True)
    complete_status = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        exclude = [
            'publish',
            'created_at',
            'updated_at',
        ]

    def get_complete_status(self, obj):
        return self.context.get("complete_status")


class LectureShortSerializer(BaseSerializer):
    resourse_count = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = ['id', 'name', 'resourse_count']

    def get_resourse_count(self, obj):
        return obj.resourse.count()


class DemoLectureSerializer(BaseSerializer):
    video = VideoSerializer(read_only=True)

    class Meta:
        model = Lecture
        fields = ['id', 'name', 'video']


class VideoSerializerV2(BaseSerializer):
    class Meta:
        model = VideoV2
        fields = ['id', 'name', 'url', 'size', 'length']


class RefImageSerializer(BaseSerializer):
    class Meta:
        model = RefImage
        fields = ['id', 'name', 'url', 'size']


class DocumentSerializer(BaseSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'url', 'size']


class SubjectiveTestSerializer(BaseSerializer):
    class Meta:
        model = SubjectiveTest
        fields = ['id', 'name', 'url', 'size']


class ChapterSerializer(BaseSerializer):
    videos = VideoSerializerV2(read_only=True, many=True)
    documents = DocumentSerializer(read_only=True, many=True)
    images = RefImageSerializer(read_only=True, many=True)
    tests = SubjectiveTestSerializer(read_only=True, many=True)

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'documents', 'videos', 'images', 'tests']