from django.urls import path

from test_series.views.api import (
    MyTestseriesView,
    TestSeriesListView,
    TestSeriesDetailView,
    TestseriesCategoryView
)

from test_series.views.testset import (
    TestsetListView,
    TestsetCountView,
    TestsetFreeListView,
    PerformanceView,
)

from test_series.views.online_test import (
    OnlineTestStartView,
    OnlineTestSubmitView,
    OnlineTestView,
    OnlineTestQuestionAnswerView,
)

api_urlpatterns = [
    # testseies apis'
    path('testseries', TestSeriesListView.as_view(), name="testseries_list"),
    path('testseries/<int:id>', TestSeriesDetailView.as_view(), name="testseries_detail"),

    # category api
    path('testseries/category', TestseriesCategoryView.as_view(), name="testseries_category"),

    # testset apis'
    path('testseries/<int:id>/testsets', TestsetListView.as_view(), name="testseries_testset"),
    path('testseries/<int:id>/testset/count', TestsetCountView.as_view(), name="testseries_testset_count"),
    path('testseries/<int:id>/testset/free', TestsetFreeListView.as_view(), name="testseries_testset_free"),
    path('testseries/<int:id>/testset/<int:testset_id>/performance', PerformanceView.as_view(), name="testset_performance"),

    # online test apis'
    path('onlinetest/<int:testset_id>/start', OnlineTestStartView.as_view(), name='online_test_start'),
    path('onlinetest/<int:onlinetest_id>', OnlineTestView.as_view(), name='online_test'),
    path('onlinetest/<int:onlinetest_id>/question', OnlineTestQuestionAnswerView.as_view(), name='online_test_question_answer'),
    path('onlinetest/<int:onlinetest_id>/submit', OnlineTestSubmitView.as_view(), name='online_test_submit'),

    # dashboard related apis'
    path('mytestseries', MyTestseriesView.as_view(), name='my_mytestseries'),
]

urlpatterns = api_urlpatterns
