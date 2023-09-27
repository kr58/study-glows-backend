from django.urls import path

from course.views.api import (
    InstructorView,
    CourseView,
    AddCourseView,
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
    AddInstructorView,
    FeatureView,
    AddChapter,
    AddVideoToChapter
)

api_urlpatterns = [
    # instructor api
    path('instructors', InstructorView.as_view(), name="instructor_list"),
    path('addinstructor', AddInstructorView.as_view(), name="add_instructor"),

    # all categories and subcategories api
    path('categories', CategoryView.as_view(), name="category_list"),

    # feature api
    path('features', FeatureView.as_view(), name="features list"),

    # course api
    path('courses', CourseView.as_view(), name="course_list"),
    path('addcourse', AddCourseView.as_view(), name="course_list"),
    path('course/<int:id>', CourseDetailView.as_view(), name="course_detail"),

    # chapter api
    path('addchapter', AddChapter.as_view(), name="add_chapter"),
    path('chapter/<int:id>/addvideo', AddVideoToChapter.as_view(), name="add_chapter"),

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
