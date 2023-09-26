from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from drf_yasg.utils import swagger_auto_schema

from account.models import UserCourseProgress
from account.utils import validateUserCourseSubscription

from utils.file_upload import upload_to_s3

from course.models import (
    Feature,
    Category,
    CoursesectionLecture,
    Instructor,
    Course,
    CourseV2,
    UserSavedCourse,
    CATEGORY_TYPE,
    CategoryEnum,
    AcademicSubCategoryEnum,
    NonAcademicSubCategoryEnum
)

from course.serializers.course_serializers import (
    InstructorSerializer, CategorySerializer,
    CourseDetailSerializer, CourseListSerializer,
    SavedCourseListSerializer, FeatureSerializer
)

from course.serializers.lecture_serializers import LectureSerializer
from course.serializers.course_section_serializers import CoursesectionDetailSerializer

from commons.responses import (
    RESPONSE_400,
    RESPONSE_404,
)

class CategoryView(APIView):
    def get(self, request):
        categoryToSubcategory = {
            CategoryEnum.ACADEMIC.value: [subject.value for subject in AcademicSubCategoryEnum],
            CategoryEnum.NONACADEMIC.value: [subject.value for subject in NonAcademicSubCategoryEnum]
        }
        return Response(categoryToSubcategory, 200)

class InstructorView(APIView):
    @swagger_auto_schema(tags=["course"], responses={200: InstructorSerializer(many=True)})
    def get(self, request):
        instructors = Instructor.objects.all()
        return Response(InstructorSerializer(instructors, many=True).data, 200)
    
class AddInstructorView(APIView):
    @swagger_auto_schema(tags=["course"], responses={200: InstructorSerializer(many=True)})
    def post(self, request):
        name = request.data["name"]
        profile_image = request.FILES["profile_image"]
        bio = request.data.get('bio', None)
        tags = request.data.get('tags', None)
        active = request.data.get('active', False)
        score = request.data.get('score', 0)
        instructor = Instructor.objects.create(
            name = name,
            profile_image = profile_image,
            bio = bio,
            tags = tags,
            active = active,
            score = score
        )
        return Response(InstructorSerializer(instructor).data, 200)

class FeatureView(APIView):
    @swagger_auto_schema(tags=["feature"], responses={200: FeatureSerializer(many=True)})
    def get(self, request):
        features = Feature.objects.all()
        return Response(FeatureSerializer(features, many=True).data, 200)

class CourseView(APIView):
    paginate_by = 6

    @swagger_auto_schema(tags=["course"], responses={200: CourseListSerializer(many=True)})
    def get(self, request):
        category_name = request.query_params.get('category')
        category_type = request.query_params.get('category_type')
        if category_name and category_name != "":
            courses = Course.objects.filter(publish=True, category__name=category_name).distinct()
        elif category_type and category_type != "":
            courses = Course.objects.filter(publish=True, category__type=category_type).distinct()
        else:
            courses = Course.objects.filter(publish=True)
        return self.pagination(courses)

    def pagination(self, courses):
        page = self.request.GET.get("page")
        paginator = Paginator(courses, self.paginate_by)
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = []
        courseListSerializer = CourseListSerializer(courses, many=True)
        return_resp = {
            "data": courseListSerializer.data,
            "total_page": paginator.num_pages,
            "per_page": paginator.per_page,
            "current_page": int(page) if page else 1
        }
        return Response(return_resp, 200)
    
class AddCourseView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["course"], responses={200: CourseListSerializer(many=True)})
    def post(self, request, *arg, **kwargs):
        title = request.data['title']
        thumbnail = request.FILES.get('thumbnail', None)
        about = request.data.get('about', None)
        language = request.data.get('language', None)
        price = request.data.get('price', None)
        mrp = request.data.get('mrp', None)
        validity = request.data.get('validity', None)
        publish = request.data.get('publish', None)
        features = request.data.get('feature', [])
        category = request.data.get('category', None)
        instructors = request.data.get('instructors', [])
        faqs = request.data.get('faq', [])
        course_section = request.data.get('coursesection', [])

        imageUrl = None
        if thumbnail != None:
            imageUrl = upload_to_s3(thumbnail, "course/thumbnail/")

        course = CourseV2.objects.create(
            title = title,
            thumbnail = imageUrl,
            about = about,
            language = language,
            price = price,
            mrp = mrp,
            validity = validity,
            publish = publish
        )
        course.feature.add(*features)
        if (category != None):
            course.category.add(category)
        course.instructor.add(*instructors)
        course.faq.add(*faqs)
        course.coursesection.add(*course_section)
        return Response({
            "message": 'success',
            'course': CourseDetailSerializer(course).data
        })

class CourseDetailView(APIView):
    message = 'Course does not exits'

    @swagger_auto_schema(tags=["course"],  responses={200: CourseDetailSerializer(many=True), 404: message})
    def get(self, request, *arg, **kwargs):
        course_id = kwargs.get('id')
        if course_id:
            course = Course.objects.filter(id=int(course_id), publish=True).first()
            if course:
                courseSerializer = CourseDetailSerializer(course, context={"user": request.user})
                return Response(courseSerializer.data, 200)
        return Response(RESPONSE_404(self.message), 404)


class CourseSectionView(APIView):
    permission_classes = (IsAuthenticated,)
    message = 'Course does not exits or subscription expired'
    message_2 = 'Course section does not exits or subscription expired'

    @swagger_auto_schema(tags=["course"])
    def get(self, request, *arg, **kwargs):
        course_id = kwargs.get('id')
        user = request.user
        if course_id:
            course = Course.objects.filter(id=int(course_id), publish=True).first()
            status, subscription = validateUserCourseSubscription(user, course)
            if course and status:
                coursesections = course.coursesection.filter(publish=True)
                if coursesections:
                    return Response({
                        "course": CourseListSerializer(course).data,
                        "section": CoursesectionDetailSerializer(coursesections, many=True, context={
                            "course": course, 
                            "user": request.user
                        }).data
                    }, 200)
                return Response(RESPONSE_404(self.message_2), 404)
            return Response(RESPONSE_404(self.message), 404)
        return Response(RESPONSE_400("fail"), 400)


class LectureDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    message = 'Course/lecture/coursesection does not exits'

    @swagger_auto_schema(tags=["course"], responses={200: LectureSerializer(), 404: message})
    def post(self, request, *arg, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_section_id = request.data.get('coursesection_id')
        lecture_id = request.data.get('lecture_id')
        if course_id and course_section_id and lecture_id:
            course = Course.objects.filter(id=int(course_id), publish=True).first()
            if course:
                status, subscription = validateUserCourseSubscription(user, course)
                if status:
                    coursesection = course.coursesection.filter(id=int(course_section_id), publish=True).first()
                    if coursesection:
                        lecture = coursesection.lecture.filter(id=int(lecture_id), publish=True).first()
                        user_course_progress = UserCourseProgress.objects.filter(
                            user=user,
                            course=course,
                            coursesection=coursesection,
                            lecture=lecture
                        ).first()
                        complete_status = True if user_course_progress else False
                        return Response(LectureSerializer(lecture, context={
                            "complete_status": complete_status,
                        }).data, 200)
                return Response('user must buy course to study', 400)
        return Response(RESPONSE_404(self.message), 404)


class LectureProgressView(APIView):
    permission_classes = (IsAuthenticated,)
    message = 'Course/lecture/coursesection does not exits'

    @swagger_auto_schema(tags=["course"], responses={200: LectureSerializer(), 404: message})
    def post(self, request, *arg, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        lecture_id = request.data.get('lecture_id')
        course_section_id = request.data.get('coursesection_id')
        if user and course_id and course_section_id and lecture_id:
            course = Course.objects.filter(id=int(course_id), publish=True).first()
            if course:
                status, subscription = validateUserCourseSubscription(user, course)
                if status:
                    coursesection = course.coursesection.filter(id=int(course_section_id), publish=True).first()
                    if coursesection:
                        lecture = coursesection.lecture.filter(id=int(lecture_id), publish=True).first()
                        if lecture:
                            user_course_progress = UserCourseProgress.objects.filter(
                                user=request.user, course=course, coursesection=coursesection, lecture=lecture
                            ).first()
                            if user_course_progress:
                                if not user_course_progress.status:
                                    user_course_progress = True
                                    user_course_progress.completed_on = timezone.now()
                                    user_course_progress.save()
                                else:
                                    return Response({'message': 'already completed'}, 400)
                            else:
                                UserCourseProgress.objects.create(
                                    user=request.user, course=course, coursesection=coursesection, lecture=lecture,
                                    status=True, completed_on=timezone.now()
                                )
                            return Response({'message': 'success'}, 200)
                return Response('user must buy course to study', 400)
        return Response(RESPONSE_404(self.message), 404)


class CategoryView(APIView):
    message = "Type does not exits."

    @swagger_auto_schema(tags=["course"],  responses={200: CategorySerializer(many=True), 400: message})
    def get(self, request, *arg, **kwargs):
        category_type = kwargs.get('type')
        if category_type in [category[0] for category in CATEGORY_TYPE]:
            courses = Course.objects.filter(publish=True, category__type=category_type).distinct().values('category')
            category_ids = [i['category'] for i in courses]
            category = Category.objects.filter(status=True, type=category_type, id__in=category_ids)
            return Response(CategorySerializer(category, many=True).data, 200)
        return Response(RESPONSE_400("fail"), 400)


class MyCourseView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["course"], responses={200: SavedCourseListSerializer(many=True)})
    def get(self, request, *arg, **kwargs):
        user = request.user
        courses = Course.objects.filter(
            id__in=user.subscription_set.filter(expire_status=False).values('course')
        )
        return Response(SavedCourseListSerializer(courses, many=True).data, 200)


class MyCourseProgressView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["course"], responses={200: ''})
    def get(self, request, *arg, **kwargs):
        user = request.user
        course_id = request.query_params.get('course_id')
        if course_id:
            courses = Course.objects.filter(id=int(course_id))
        else:
            courses = Course.objects.filter(
                id__in=user.subscription_set.filter(expire_status=False).values('course')
            )
        if courses:
            course_progress_list = []
            for course in courses:
                course_progress = self.get_course_progress(course, user)
                course_progress_list.append({
                    "course": CourseListSerializer(course).data,
                    "progress": course_progress
                })
            return Response(course_progress_list, 200)
        return Response(RESPONSE_400("course not found"), 400)

    def get_course_progress(self, course, user):
        total_lectures = CoursesectionLecture.objects.filter(
            publish=True,
            coursesection__in=course.coursesection.filter(publish=True)
        ).count()
        user_completed_lectures = UserCourseProgress.objects.filter(
            user=user,
            status=True,
            course=course
        ).count()
        if total_lectures > 0:
            return (user_completed_lectures * 100)//total_lectures
        return ""


class SavedCourseView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        courses = Course.objects.filter(id__in=user.usersavedcourse_set.all().values('course'))
        return Response(SavedCourseListSerializer(courses, many=True).data, 200)


class SaveCourse(APIView):
    permission_classes = (IsAuthenticated,)

    @ swagger_auto_schema(tags=["course"], responses={200: "success", 400: "fail"})
    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('id')
        if course_id:
            course = Course.objects.filter(id=int(course_id)).first()
            if course:
                UserSavedCourse.objects.update_or_create(
                    user=request.user, course=course,
                    defaults={"user": request.user, "course": course}
                )
                return Response({
                    "message": "success",
                }, 200)
        return Response({"message": "fail"}, 400)


class UnsaveCourse(APIView):
    permission_classes = (IsAuthenticated,)

    @ swagger_auto_schema(tags=["course"], responses={200: "success", 400: "fail"})
    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('id')
        if course_id:
            course = Course.objects.filter(id=int(course_id)).first()
            if course:
                UserSavedCourse.objects.filter(user=request.user, course=course).delete()
                return Response({
                    "message": "success",
                }, 200)
        return Response({"message": "fail"}, 400)
