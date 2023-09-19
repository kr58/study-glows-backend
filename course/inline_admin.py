from django.contrib import admin


from course.models import (
    Course,
    CourseSection,
)

class FeatureInLine(admin.TabularInline):
    model = Course.feature.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Course Features"
    autocomplete_fields = ('feature',)
    classes = ['collapse']


class CategoryInline(admin.TabularInline):
    model = Course.category.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Course category"
    autocomplete_fields = ('category',)
    classes = ['collapse']


class FAQInline(admin.TabularInline):
    model = Course.faq.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Course FAQ"
    autocomplete_fields = ('faq',)
    classes = ['collapse']


class InstructorInline(admin.TabularInline):
    model = Course.instructor.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Course Instructor"
    autocomplete_fields = ('instructor',)
    classes = ['collapse']


class CoursesectionInline(admin.TabularInline):
    model = Course.coursesection.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Course Sections/Curriculum"
    autocomplete_fields = ('coursesection',)
    classes = ['collapse']



class CoursesectionLectureInLine(admin.TabularInline):
    model = CourseSection.lecture.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Lectures"
    autocomplete_fields = ('lecture',)
    # exclude = ('publish',)

