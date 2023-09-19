from django.urls import path

from course.views.api import (
    InstructorView,
    CourseView,
    CourseDetailView,
    CategoryView,
    MyCourseView,
    SavedCourseView,
    SaveCourse,
    UnsaveCourse,
    CourseSectionView,
    LectureDetailView,
    LectureProgressView,
    MyCourseProgressView,
)

api_urlpatterns = [
    path('instructors', InstructorView.as_view(), name="instructor_list"),

    # course api
    path('courses', CourseView.as_view(), name="course_list"),
    path('course/<int:id>', CourseDetailView.as_view(), name="course_detail"),

    # category api
    path('course/<str:type>/category', CategoryView.as_view(), name="course_category"),

    # saved, unsave course's api
    path('course/saved', SavedCourseView.as_view(), name='course_saved'),
    path('course/<int:id>/save', SaveCourse.as_view(), name='course_save'),
    path('course/<int:id>/unsave', UnsaveCourse.as_view(), name='course_unsave'),

    # dashboard related api's
    path('mycourses', MyCourseView.as_view(), name='my_course'),
    path('mycourses/progress', MyCourseProgressView.as_view(), name='my_course_progress'),

    # study
    path('study/mycourses/<int:id>/coursesection', CourseSectionView.as_view(), name='my_course_section'),
    path('study/mycourses/lecture', LectureDetailView.as_view(), name='lecture_detail'),

    # lecture course progress
    path('study/mycourses/lecture/progress', LectureProgressView.as_view(), name='lecture_progress'),
]

urlpatterns = api_urlpatterns
