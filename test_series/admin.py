from django.contrib import admin
from test_series.models import (
    Option,
    Category,
    Feature,
    Feature2,
    Question,
    TestSeries,
    TestSetCategory,
    Testset
)

from test_series.inline_admin import (
    OptionInline,
    CategoryInline,
    FAQInline,
    FeatureInLine,
    Feature2InLine,
    QuestionInline,
    TestsetCategoryInline,
    TestsetInine
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', )
    list_filter = ('status', )
    search_fields = ('name', )


class TestSeriesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price', 'publish',)
    list_filter = ('publish',)
    exclude = ('feature', 'feature2', 'category', 'faq', 'testset')
    search_fields = ('name',)
    inlines = [
        FeatureInLine,
        Feature2InLine,
        CategoryInline,
        FAQInline,
        TestsetInine,
    ]


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    list_filter = ('status', )
    search_fields = ('name', )


class Feature2Admin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'icon')
    list_filter = ('status', )
    search_fields = ('name', )


class TestSetCategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'publish')
    list_filter = ('publish', )
    search_fields = ('name',)


class TestsetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'publish')
    list_filter = ('publish', )
    exclude = ('testset_category', 'description', 'order')
    search_fields = ('name',)
    inlines = [
        TestsetCategoryInline,
        QuestionInline
    ]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'question')
    list_filter = ('difficulty',)
    search_fields = ('type', 'question')
    exclude = ('max_time', )
    inlines = [
        OptionInline
    ]


admin.site.register(TestSeries, TestSeriesAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Feature2, Feature2Admin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(TestSetCategory, TestSetCategoryAdmin)
admin.site.register(Testset, TestsetAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
