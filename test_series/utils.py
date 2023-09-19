
from account.models import UserTestset


def validate_user_onlinetest(user, onlinetest_id):
    user_testset = UserTestset.objects.filter(id=int(onlinetest_id)).first()
    if user_testset and user_testset.user == user:
        return True, user_testset
    return False, None
