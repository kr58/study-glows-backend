import json
from test_series.models import TestsetQuestion
from account.models import Subscription, UserTestsetAnswer


def validateUserCourseSubscription(user, course):
    if user and course:
        subcription = Subscription.objects.filter(
            user=user, course=course, expire_status=False
        ).first()
        if subcription:
            return True, course
    return False, None


def validateUserTestseriesSubscription(user, testseries):
    if user and testseries:
        subcription = Subscription.objects.filter(
            user=user, testseries=testseries, expire_status=False
        ).first()
        if subcription:
            return True, subcription
    return False, None


def initializeUserTestsetAnswer(user_testset, status='not_visited'):
    testset = user_testset.testset
    if testset and user_testset:
        testset_questions = TestsetQuestion.objects.filter(testset=testset, publish=True)
        for testset_question in testset_questions:
            UserTestsetAnswer.objects.create(
                user_testset=user_testset,
                question=testset_question.question,
                status=status
            )
        if testset_questions.count() > 0:
            return True
    return False


def checkUserTestsetAnswer(user_testset):
    testset = user_testset.testset
    if testset and user_testset and user_testset.completed:
        user_testset_answers = user_testset.usertestsetanswer_set.all()
        for answer in user_testset_answers:
            question = answer.question
            if question.type == "mcq":
                if answer.selected_option:
                    _option = question.option_set.filter(id=answer.selected_option.id).first()
                    if _option:
                        answer.marks_awarded = _option.marks
                        answer.selected_option_status = _option.correct_status
                        answer.check_status = True
                        answer.save()
                else:
                    _option = question.option_set.filter(correct_status=False).first()
                    if _option:
                        answer.marks_awarded = _option.marks
                        answer.selected_option_status = _option.correct_status
                        answer.check_status = True
                        answer.save()
        return True
    return False


def calutateUserTestsetAnswer(user_testset):
    testset = user_testset.testset
    if testset and user_testset and user_testset.completed:
        _report_data = {
            "score": 0,
            "correct": 0,
            "incorrect": 0,
            "attempted": 0,
            "totalScore": 0,
            "totalQuestion": 0,
        }
        total_checked = 0
        user_testset_answers = user_testset.usertestsetanswer_set.all()
        for answer in user_testset_answers:
            if answer.check_status:
                _report_data["score"] += answer.marks_awarded
                if answer.selected_option_status:
                    _report_data["correct"] += 1
                if not answer.selected_option_status and answer.status in ["answered", "review_marked"]:
                    _report_data["incorrect"] += 1
                if answer.status != "not_visited":
                    _report_data["attempted"] += 1
                total_checked += 1
            _report_data["totalQuestion"] += 1
            _report_data["totalScore"] += answer.question.marks
        if total_checked == _report_data["totalQuestion"]:
            user_testset.report_generated = "generated"
        else:
            user_testset.report_generated = "incomplete"
        user_testset.report_data = json.dumps(_report_data)
        user_testset.save()
        return True
    return False
