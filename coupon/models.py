from django.db import models
from commons.models import TimeStampedModel

from course.models import Course, Category as course_Category
from test_series.models import TestSeries, Category as test_series_Category

METHOD_CHOICES = (
    ('percent', 'percent'),
    ('fixed_amount', 'Fixed Amout'),
)


class Coupon(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    method = models.CharField(choices=METHOD_CHOICES, default='percent', max_length=20)
    value = models.PositiveIntegerField(default=0)
    usage_limit = models.PositiveIntegerField(default=0)
    used = models.PositiveIntegerField(default=0)
    course_category = models.ManyToManyField(course_Category, blank=True)
    testseries_category = models.ManyToManyField(test_series_Category, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    testseries = models.ManyToManyField(TestSeries, blank=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return self.name
