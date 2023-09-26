from django.db import models
import datetime
from commons.models import TimeStampedModel
from account.models import FAQ, User
from enum import Enum
from django_enum import EnumField

CATEGORY_TYPE = (
    ('Academic', 'Academic'),
    ('NonAcademic', 'NonAcademic')
)

class CategoryEnum(Enum):
    ACADEMIC = 'Academic'
    NONACADEMIC = 'Non-Academic'

class AcademicSubCategoryEnum(Enum):
    ACADEMIC1 = "academic1"
    ACADEMIC2 = "academic2"
    ACADEMIC3 = "academic3"
    ACADEMIC4 = "academic4"
    ACADEMIC5 = "academic5"
    ACADEMIC6 = "academic6"
    ACADEMIC7 = "academic7"
    ACADEMIC8 = "academic8"

class NonAcademicSubCategoryEnum(Enum):
    NONACADEMIC1 = "non-academic1"
    NONACADEMIC2 = "non-academic2"
    NONACADEMIC3 = "non-academic3"
    NONACADEMIC4 = "non-academic4"
    NONACADEMIC5 = "non-academic5"

COURSE_LANGUAGE = (
    ('English', 'English'),
    ('Hindi', 'Hindi'),
    ('Hinglish', 'Hinglish')
)

RESOURCE_TYPE = (
    ('project', 'project'),
    ('notes', 'notes'),
    ('link', 'link'),
)


class Instructor(TimeStampedModel):
    name = models.CharField(max_length=512, blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to='instructor/%Y%m%d')
    bio = models.CharField(max_length=2048, blank=True, null=True)
    tags = models.CharField(max_length=2048, blank=True, null=True)
    active = models.BooleanField(default=True)
    score = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else str(self.pk)

    class Meta:
        ordering = ("-created_at", "score")


class Category(TimeStampedModel):
    name = models.CharField(max_length=216, blank=True, null=True)
    type = models.CharField(max_length=216, blank=True, null=True, choices=CATEGORY_TYPE)
    description = models.CharField(max_length=1024, blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}' if self.name else str(self.pk)

    class Meta:
        ordering = ("-created_at", "order")


class Feature(TimeStampedModel):
    name = models.CharField(max_length=216, blank=True, null=True)
    icon = models.FileField(blank=True, null=True, upload_to='icon/%Y%m%d')
    status = models.BooleanField(default=True, blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else str(self.pk)

    class Meta:
        ordering = ("-created_at", "order")


class Video(TimeStampedModel):
    name = models.CharField(max_length=2048, blank=True, null=True)
    video = models.FileField(blank=True, null=True, upload_to='course/video/%Y%m%d')
    length = models.PositiveIntegerField(blank=True, null=True)
    hls_video = models.URLField(blank=True, null=True)
    hls_status = models.BooleanField(default=False, blank=True, null=True)
    hls_updated_at = models.DateTimeField(blank=True, null=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.name if self.name else f'video#{self.pk}'


class Resources(TimeStampedModel):
    name = models.CharField(max_length=512, blank=True, null=True)
    type = models.CharField(max_length=512, blank=True, null=True, choices=RESOURCE_TYPE)
    project = models.TextField(blank=True, null=True)
    notes = models.FileField(blank=True, null=True, upload_to='course/resourse/notes/%Y%m%d')
    link = models.URLField(blank=True, null=True)
    extra = models.TextField(blank=True, null=True)
    publish = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else f'resourse#{self.pk}'


class Lecture(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    video = models.OneToOneField(Video, on_delete=models.DO_NOTHING, blank=True, null=True)
    resourse = models.ManyToManyField(Resources, blank=True)
    publish = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else f'lecture#{self.pk}'


class CourseSection(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    publish = models.BooleanField(default=False, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    lecture = models.ManyToManyField(Lecture, blank=True, through='coursesectionlecture')

    def __str__(self):
        return self.name if self.name else f'section#{self.pk}'


class CoursesectionLecture(TimeStampedModel):
    order = models.PositiveIntegerField(default=1, blank=True, null=True)
    coursesection = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    is_demo = models.BooleanField(default=False, blank=True, null=True)
    publish = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ('order',)


class Course(TimeStampedModel):
    title = models.CharField(max_length=1024, blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True, upload_to='course/thumbnail/%Y%m%d')
    thumbnail2 = models.ImageField(blank=True, null=True, upload_to='course/thumbnail/%Y%m%d')
    about = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=512, blank=True, null=True, choices=COURSE_LANGUAGE)
    price = models.FloatField(blank=True, null=True, default=0)
    mrp = models.FloatField(blank=True, null=True, default=0)
    validity = models.DateField(blank=True, null=True)
    publish = models.BooleanField(default=True, blank=True, null=True)
    feature = models.ManyToManyField(Feature, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    instructor = models.ManyToManyField(Instructor, blank=True)
    faq = models.ManyToManyField(FAQ, blank=True)
    coursesection = models.ManyToManyField(CourseSection, blank=True)

    def __str__(self):
        return self.title if self.title else str(self.pk)

    class Meta:
        ordering = ("-created_at",)


class CourseV2(TimeStampedModel):
    title = models.CharField(max_length=1024, blank=True, null=True)
    thumbnail = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=512, blank=True, null=True, choices=COURSE_LANGUAGE)
    price = models.FloatField(blank=True, null=True, default=0)
    mrp = models.FloatField(blank=True, null=True, default=0)
    validity = models.DateField(default=datetime.datetime.now, blank=True, null=True)
    publish = models.DateField(default=datetime.datetime.now, blank=True, null=True)
    feature = models.ManyToManyField(Feature, blank=True)
    category = EnumField(CategoryEnum, blank=True)
    instructor = models.ManyToManyField(Instructor, blank=True)
    faq = models.ManyToManyField(FAQ, blank=True)
    coursesection = models.ManyToManyField(CourseSection, blank=True)

    def __str__(self):
        return self.title if self.title else str(self.pk)

    class Meta:
        ordering = ("-created_at",)


class UserSavedCourse(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.course and self.user:
            return f"course_user {str(self.course.pk)}, {str(self.user.pk)}"
        return str(self.pk)
