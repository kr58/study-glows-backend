from django.db import models
from account.models import FAQ

from commons.models import TimeStampedModel
from test_series.constants import (
    TESTSERIES_LANGUAGE,
    TESTSERIES_ACCESS_TYPE,
    TESTSET_TYPE,
    QUESTION_TYPE,
    QUESTION_DIFFICULTY
)


class Question(TimeStampedModel):
    type = models.CharField(max_length=512, blank=True, null=True, choices=QUESTION_TYPE)
    marks = models.FloatField(blank=True, null=True)
    max_time = models.PositiveIntegerField(blank=True, null=True)
    difficulty = models.CharField(max_length=512, blank=True, null=True, choices=QUESTION_DIFFICULTY)
    question = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question if self.question else f'question#{self.pk}'


class Option(TimeStampedModel):
    question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE)
    option = models.CharField(max_length=512, blank=True, null=True)
    correct_status = models.BooleanField(default=False, blank=True, null=True)
    marks = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return self.option if self.option else f'option#{self.pk}'


class TestSetCategory(TimeStampedModel):
    name = models.CharField(max_length=512, blank=True, null=True)
    publish = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name}" if self.name else f'testset_category#{self.pk}'


class Testset(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    language = models.CharField(max_length=512, blank=True, null=True, choices=TESTSERIES_LANGUAGE)
    description = models.TextField(blank=True, null=True)
    access_type = models.CharField(max_length=512, blank=True, null=True, choices=TESTSERIES_ACCESS_TYPE)
    duration = models.PositiveIntegerField(blank=True, null=True)
    type = models.CharField(max_length=512, blank=True, null=True, choices=TESTSET_TYPE)
    testset_category = models.ManyToManyField(TestSetCategory, blank=True)
    order = models.PositiveIntegerField(blank=True, null=True)
    publish = models.BooleanField(default=True)
    questions = models.ManyToManyField(Question, blank=True, through='testsetquestion')

    def __str__(self):
        return self.name if self.name else str(self.pk)

    class Meta:
        ordering = ("-created_at", "order")


class TestsetQuestion(TimeStampedModel):
    testset = models.ForeignKey(Testset, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    section = models.CharField(max_length=1024, blank=True, null=True)
    order = models.PositiveIntegerField(default=1, blank=True, null=True)
    publish = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ('order',)


class Category(TimeStampedModel):
    name = models.CharField(max_length=216, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}' if self.name else str(self.pk)

    class Meta:
        ordering = ("-created_at", "order")


class Feature(TimeStampedModel):
    name = models.CharField(max_length=216, blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else str(self.pk)

    class Meta:
        ordering = ("-created_at", "order")


class Feature2(TimeStampedModel):
    name = models.CharField(max_length=216, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    icon = models.FileField(blank=True, null=True, upload_to='icon/%Y%m%d')
    status = models.BooleanField(default=True, blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else str(self.pk)

    class Meta:
        ordering = ("-created_at", "order")


class TestSeries(TimeStampedModel):
    title = models.CharField(max_length=512, blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True, upload_to='testSeries/thumbnail/%Y%m%d')
    thumbnail2 = models.ImageField(blank=True, null=True, upload_to='testSeries/thumbnail/%Y%m%d')
    about = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=512, blank=True, null=True, choices=TESTSERIES_LANGUAGE)
    price = models.FloatField(blank=True, null=True, default=0)
    mrp = models.FloatField(blank=True, null=True, default=0)
    validity = models.DateField(blank=True, null=True)
    publish = models.BooleanField(default=True, blank=True, null=True)
    feature = models.ManyToManyField(Feature, blank=True)
    feature2 = models.ManyToManyField(Feature2, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    faq = models.ManyToManyField(FAQ, blank=True)
    testset = models.ManyToManyField(Testset, blank=True)

    def __str__(self):
        return self.title if self.title else str(self.pk)

    class Meta:
        ordering = ("-created_at",)
