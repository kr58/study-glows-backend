import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from account.models import UserTestset

from test_series.models import (
    TESTSET_TYPE,
    Question,
    TestSeries,
    TestSetCategory,
    Testset
)
from test_series.serializers import (
    TestSeriesListSerializer,
    TestsetCategroySerializer,
    TestsetDetailSerializer,
    TestsetListSerializer,
)

from commons.responses import (
    RESPONSE_404,
    RESPONSE_400,
)


class TestsetCountView(APIView):
    message = 'Testseries does not exits'

    def get(self, request, *arg, **kwargs):
        testseries_id = kwargs.get('id')
        if testseries_id:
            testseries = TestSeries.objects.filter(id=int(testseries_id), publish=True).first()
            if testseries:
                testsets = testseries.testset.filter(publish=True).values('type')
                testset_type_count = {
                    'chapter': 0,
                    'subject': 0,
                    'full': 0,
                    'live': 0,
                    None: 0
                }
                for testset in testsets:
                    testset_type_count[testset.get('type')] += 1
                return Response({
                    "testseries": TestSeriesListSerializer(testseries).data,
                    "type": dict(testset_type_count)
                }, 200)
        return Response(RESPONSE_404(self.message), 404)


class TestsetListView(APIView):
    paginate_by = 1

    @swagger_auto_schema(tags=["testseries"])
    def get(self, request, *arg, **kwargs):
        testseries_id = kwargs.get('id')
        testset_type = request.query_params.get('type')
        user = request.user
        if testseries_id:
            testseries = TestSeries.objects.filter(id=int(testseries_id), publish=True).first()
            if testseries:
                if testset_type:
                    testsets = testseries.testset.filter(publish=True, type=testset_type)
                else:
                    testsets = testseries.testset.filter(publish=True)
                return self.pagination(testsets, user)

    def pagination(self, testsets, user):
        page = self.request.GET.get("page")
        testset_category = TestSetCategory.objects.filter(testset__in=testsets).distinct()
        paginator = Paginator(testsets, self.paginate_by)
        try:
            testsets = paginator.page(page)
        except PageNotAnInteger:
            testsets = paginator.page(1)
        except EmptyPage:
            testsets = []
        return_resp = {
            "data": TestsetListSerializer(testsets, many=True, context={"user": user}).data,
            "category": TestsetCategroySerializer(testset_category, many=True).data,
            "total_page": paginator.num_pages,
            "per_page": paginator.per_page,
            "current_page": int(page) if page else 1
        }
        return Response(return_resp, 200)


class TestsetFreeListView(APIView):

    @swagger_auto_schema(tags=["testseries"])
    def get(self, request, *arg, **kwargs):
        testseries_id = kwargs.get('id')
        if testseries_id:
            testseries = TestSeries.objects.filter(id=int(testseries_id), publish=True).first()
            if testseries:
                testsets = testseries.testset.filter(publish=True, access_type='free')
                return Response(TestsetListSerializer(testsets, many=True).data, 200)
        return Response(RESPONSE_400("error"), 400)


class PerformanceView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["testseries"])
    def get(self, request, *arg, **kwargs):
        testset_id = kwargs.get('testset_id')
        user = request.user
        if testset_id and user:
            testset = Testset.objects.filter(id=int(testset_id), publish=True).first()
            if testset:
                user_testset = UserTestset.objects.filter(
                    user=user,
                    testset=testset,
                    completed=True
                ).order_by('-end_at').first()
                if user_testset:
                    if user_testset.report_generated != "complete":
                        user_testset.checkUserTestsetAnswer()
                        user_testset.calutateUserTestsetAnswer()
                    report_data = json.loads(user_testset.report_data)
                    resp = {
                        "performanceData": {
                            "reportData": report_data,
                            "reportStatus": user_testset.report_generated,
                        },
                        "message": "success"
                    }
                    return Response(resp, 200)
        return Response(RESPONSE_400("error"), 400)
