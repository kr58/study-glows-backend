from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.models import UserTestset, UserTestsetAnswer
from account.constants import QUESTION_ANSWER_STATUS
from account.utils import validateUserTestseriesSubscription
from commons.responses import RESPONSE_400
from test_series.constants import TESTSERIES_ACCESS_TYPE

from test_series.models import Option, TestSeries, Testset
from test_series.serializers import OnlineTestSerializer
from account.serializers import UserTestsetAnswerDetailSerializer, UserTestsetAnswerListSerializer
from test_series.utils import validate_user_onlinetest


class OnlineTestStartView(APIView):
    permission_classes = (IsAuthenticated,)
    message_not_subscribed = "user is not subscribed for this testset"
    message_error = "error"

    def post(self, request, *arg, **kwargs):
        testseries_id = request.data.get('testseries_id')
        testset_id = kwargs.get('testset_id')
        if testseries_id:
            testseries = TestSeries.objects.filter(id=int(testseries_id)).first()
            testset = Testset.objects.filter(id=int(testset_id)).first()
            if testseries and testset and testset.access_type in [i[0] for i in TESTSERIES_ACCESS_TYPE]:
                # if testset is paid
                if testset.access_type == 'paid':
                    subscription_status, subscription = validateUserTestseriesSubscription(request.user, testseries)
                    if not subscription_status:
                        return Response(RESPONSE_400(self.message_not_subscribed), 400)
                    status, user_testset = self.get_or_create_user_testset(request, testset, testseries)

                # if testset is free
                if testset.access_type == 'free':
                    status, user_testset = self.get_or_create_user_testset(request, testset, testseries)
                    print(status, user_testset)
                if status:
                    resp = {"message": "success", "onlineTestId": user_testset.id}
                    return Response(resp, 200)
        return Response(RESPONSE_400(self.message_error), 400)

    def get_or_create_user_testset(self, request, testset, testseries):
        if testseries and testset:
            user_testset = UserTestset.objects.filter(
                user=request.user,
                testset=testset,
                testseries=testseries,
                completed=False
            ).first()

            # check if testset is ended or not
            if user_testset and user_testset.started_at and testset.duration:
                datetime_now = timezone.now()
                aspected_end_at = user_testset.started_at + timedelta(minutes=testset.duration)
                if datetime_now >= aspected_end_at:
                    user_testset.end_at = aspected_end_at
                    user_testset.completed = True
                    user_testset.save()
                    user_testset = None  # make user_testset none so it will be created again

            if not user_testset:
                user_testset = UserTestset.objects.create(
                    user=request.user,
                    testset=testset,
                    testseries=testseries,
                    started_at=timezone.now()
                )
                # create usertestsetanswer
                user_testset.initializeUserTestsetAnswer()
            return True, user_testset
        return False, None


class OnlineTestView(APIView):
    permission_classes = (IsAuthenticated,)
    message_error = "error"

    def get(self, request, *arg, **kwargs):
        onlinetest_id = kwargs.get("onlinetest_id")
        if onlinetest_id:
            status, user_testset = validate_user_onlinetest(request.user, onlinetest_id)
            if status and not user_testset.completed:
                user_testset_answer_sheet = UserTestsetAnswer.objects.filter(user_testset=user_testset)
                resp = {
                    "onlinetest": OnlineTestSerializer(user_testset).data,
                    "questionsAnswer": UserTestsetAnswerListSerializer(user_testset_answer_sheet, many=True).data
                }
                return Response(resp, 200)
        return Response(RESPONSE_400(self.message_error), 400)


class OnlineTestQuestionAnswerView(APIView):
    permission_classes = (IsAuthenticated,)
    message_error = "error"

    def get(self, request, *arg, **kwargs):
        onlinetest_id = kwargs.get("onlinetest_id")
        user_testset_answer_sheet_id = request.query_params.get('questionAnswer_id')
        if onlinetest_id and user_testset_answer_sheet_id:
            status, user_testset = validate_user_onlinetest(request.user, onlinetest_id)
            if status and not user_testset.completed:
                user_testset_answer_sheet = UserTestsetAnswer.objects.filter(id=int(user_testset_answer_sheet_id)).first()
                if user_testset_answer_sheet and user_testset_answer_sheet.question:
                    return Response(UserTestsetAnswerDetailSerializer(user_testset_answer_sheet).data, 200)
        return Response(RESPONSE_400(self.message_error), 400)

    def post(self, request, *arg, **kwargs):
        onlinetest_id = kwargs.get("onlinetest_id")
        user_testset_answer_sheet_id = request.data.get('questionAnswer_id')
        if onlinetest_id and user_testset_answer_sheet_id:
            status, user_testset = validate_user_onlinetest(request.user, onlinetest_id)
            if status and not user_testset.completed:
                user_testset_answer_sheet = UserTestsetAnswer.objects.filter(id=int(user_testset_answer_sheet_id)).first()
                return self.update_testset_answer(user_testset_answer_sheet, request)
        return Response(RESPONSE_400(self.message_error), 400)

    def update_testset_answer(self, user_testset_answer_sheet, request):
        option_id = request.data.get('option_id')
        answer = request.data.get('answer')
        question_status = request.data.get('question_status')
        if question_status and question_status in [i[0] for i in QUESTION_ANSWER_STATUS]:
            if question_status == "answered" or question_status == "review_marked":
                question = user_testset_answer_sheet.question
                if question and question.type == "mcq":
                    option = Option.objects.filter(id=int(option_id)).first()
                    if not option:
                        return Response(RESPONSE_400("invalid option"), 400)
                    user_testset_answer_sheet.selected_option = option
                    user_testset_answer_sheet.status = question_status
                    user_testset_answer_sheet.save()
                    return Response(UserTestsetAnswerDetailSerializer(user_testset_answer_sheet).data, 200)
                elif question and question.type == "cq":
                    user_testset_answer_sheet.answer = answer
                    user_testset_answer_sheet.status = question_status
                    user_testset_answer_sheet.save()
                    return Response(UserTestsetAnswerDetailSerializer(user_testset_answer_sheet).data, 200)
            elif question_status == "not_answer":
                user_testset_answer_sheet.answer = None
                user_testset_answer_sheet.selected_option = None
                user_testset_answer_sheet.status = question_status
                user_testset_answer_sheet.save()
                return Response(UserTestsetAnswerDetailSerializer(user_testset_answer_sheet).data, 200)
            return Response(RESPONSE_400("error"), 400)
        return Response(RESPONSE_400("invalid question_status"), 400)


class OnlineTestSubmitView(APIView):
    permission_classes = (IsAuthenticated,)
    message_error = "error"

    def post(self, request, *arg, **kwargs):
        onlinetest_id = kwargs.get("onlinetest_id")
        if onlinetest_id:
            status, user_testset = validate_user_onlinetest(request.user, onlinetest_id)
            if status and not user_testset.completed:
                user_testset.end_at = timezone.now()
                user_testset.completed = True
                user_testset.save()
                self.after_submiting_test(user_testset)
                return Response({"message": "success"}, 200)
        return Response(RESPONSE_400(self.message_error), 400)

    def after_submiting_test(self, user_testset):
        pass
