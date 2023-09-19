from django.contrib import admin

from course.models import (
    CourseSection,
    Instructor,
    Feature,
    Category,
    Course,
    Lecture,
    Resources,
    UserSavedCourse,
    Video,
)

from course.inline_admin import (
    CoursesectionInline,
    CoursesectionLectureInLine,
    FeatureInLine,
    FAQInline,
    InstructorInline,
    CategoryInline,
)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'type', 'status', )
    list_filter = ('status', 'type')
    search_fields = ('name', )


class CourseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'language', 'price', 'publish')
    list_filter = ('publish', 'category')
    search_fields = ('title', )
    exclude = ('coursesection', 'feature', 'instructor', 'faq', 'category')
    inlines = [
        FeatureInLine,
        FAQInline,
        InstructorInline,
        CategoryInline,
        CoursesectionInline,
    ]


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'icon')
    list_filter = ('status', )
    search_fields = ('name', )


class InstructorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'active')
    list_filter = ('active', )
    search_fields = ('name', )


class UserSavedCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')

class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish')
    list_filter = ('publish', 'course__category')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', 'id')
    autocomplete_fields = ('course',)
    fieldsets = (
        (None, {
            'fields': (
                'name',
                # 'description',        
                'publish',        
            )
        }),
        ('Others Detail', {
            'classes': ('collapse',),
            'fields': (
                'created_at',
                'updated_at',
                'created_by',
            ),
        })
    )
    inlines = [
        CoursesectionLectureInLine
    ]


class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'video', 'publish')
    list_filter = ('publish',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'video',        
                'publish',        
            )
        }),
        ('Others Detail', {
            'classes': ('collapse',),
            'fields': (
                'length',
                'hls_video',
                'hls_status',
                'hls_updated_at',
                'created_at',
                'updated_at',
            ),
        })
    )

class LectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish')
    list_filter = ('publish', )
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('video',)
    filter_horizontal = ('resourse',)
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'publish'),
                'video',
                'overview',
                'resourse'
            )
        }),
        ('Others Detail', {
            'classes': ('collapse',),
            'fields': (
                'created_at',
                'updated_at',
            ),
        })
    )

class ResourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'publish')
    list_filter = ('type', 'publish')
    exclude = ('extra',)


admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserSavedCourse, UserSavedCourseAdmin)
admin.site.register(CourseSection, CourseSectionAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Resources, ResourseAdmin)
