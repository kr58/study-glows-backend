from django.contrib import admin

from test_series.models import (
    Option,
    TestSeries,
    Testset
)


class FeatureInLine(admin.TabularInline):
    model = TestSeries.feature.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Features"
    autocomplete_fields = ('feature',)
    classes = ['collapse']


class Feature2InLine(admin.TabularInline):
    model = TestSeries.feature2.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Features 2"
    autocomplete_fields = ('feature2',)
    classes = ['collapse']


class CategoryInline(admin.TabularInline):
    model = TestSeries.category.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Category"
    autocomplete_fields = ('category',)
    classes = ['collapse']


class FAQInline(admin.TabularInline):
    model = TestSeries.faq.through
    extra = 0
    min_num = 1
    verbose_name_plural = "FAQ"
    autocomplete_fields = ('faq',)
    classes = ['collapse']


class TestsetInine(admin.TabularInline):
    model = TestSeries.testset.through
    extra = 0
    min_num = 0
    verbose_name_plural = "Test Sets"
    autocomplete_fields = ('testset',)
    classes = ['collapse']


class TestsetCategoryInline(admin.TabularInline):
    model = Testset.testset_category.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Test set catgeory"
    classes = ['collapse']


class OptionInline(admin.TabularInline):
    model = Option
    extra = 0
    min_num = 1
    verbose_name_plural = "Option"


class QuestionInline(admin.TabularInline):
    model = Testset.questions.through
    extra = 0
    min_num = 1
    verbose_name_plural = "Questions"
    autocomplete_fields = ('question',)
    classes = ['collapse']
