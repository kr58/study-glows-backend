from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from test_series.models import (
    TESTSET_TYPE,
    Category,
    TestSeries
)
from test_series.serializers import (
    TestSeriesDetailSerializer,
    TestSeriesListSerializer,
    TestseriesCategorySerializer,
)

from commons.responses import (
    RESPONSE_404,
    RESPONSE_400,
)


class TestSeriesListView(APIView):
    paginate_by = 6

    def get(self, request):
        # print(request.query_params)
        category_name = request.query_params.get('category')
        category_type = request.query_params.get('category_type')
        if category_name and category_name != "":
            testSeries = TestSeries.objects.filter(publish=True, category__name=category_name).distinct()
        elif category_type and category_type != "":
            testSeries = TestSeries.objects.filter(publish=True, category__type=category_type).distinct()
        else:
            testSeries = TestSeries.objects.filter(publish=True)
        return self.pagination(testSeries)

    def pagination(self, testseries):
        page = self.request.GET.get("page")
        paginator = Paginator(testseries, self.paginate_by)
        try:
            testseries = paginator.page(page)
        except PageNotAnInteger:
            testseries = paginator.page(1)
        except EmptyPage:
            testseries = []
        testSeriesListSerializer = TestSeriesListSerializer(testseries, many=True)
        return_resp = {
            "data": testSeriesListSerializer.data,
            "total_page": paginator.num_pages,
            "per_page": paginator.per_page,
            "current_page": int(page) if page else 1
        }
        return Response(return_resp, 200)


class TestSeriesDetailView(APIView):
    message = 'Testseries does not exits'

    def get(self, request, *arg, **kwargs):
        testseries_id = kwargs.get('id')
        if testseries_id:
            testseries = TestSeries.objects.filter(id=int(testseries_id), publish=True).first()
            if testseries:
                testseriesSerializer = TestSeriesDetailSerializer(testseries, context={"user": request.user})
                return Response(testseriesSerializer.data, 200)
        return Response(RESPONSE_404(self.message), 404)


class TestseriesCategoryView(APIView):

    @swagger_auto_schema(tags=["testseries"],  responses={200: TestseriesCategorySerializer(many=True)})
    def get(self, request, *arg, **kwargs):
        category = Category.objects.filter(status=True)
        return Response(TestseriesCategorySerializer(category, many=True).data, 200)


class MyTestseriesView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["testseries"], responses={200: TestSeriesListSerializer(many=True)})
    def get(self, request, *arg, **kwargs):
        user = request.user
        testseries = TestSeries.objects.filter(
            id__in=user.subscription_set.filter(expire_status=False).values('testseries')
        )
        return Response(TestSeriesListSerializer(testseries, many=True).data, 200)
