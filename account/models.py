import phonenumbers
from django.db import models
from django.core import validators
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from commons.models import TimeStampedModel
from commons.constants import PRODUCT_TYPE
from account.constants import (
    FAQ_TYPE,
    QUESTION_ANSWER_STATUS,
    USER_TESTSET_REPORT_STATUS,
)


def normalize_phone(phone, country_code=None):
    phone = phone.strip().lower()
    phone_number = phonenumbers.parse(phone, country_code)
    phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
    return phone


class UserManager(BaseUserManager):
    def _create_user(self, email_or_phone, password, **extra_fields):
        if not email_or_phone:
            raise ValueError('The given email_or_phone must be set')

        if "@" in email_or_phone:
            email_or_phone = self.normalize_email(email_or_phone)
            username, email, phone = (email_or_phone, email_or_phone, "")
        else:
            email_or_phone = normalize_phone(email_or_phone, country_code=extra_fields.get("country_code"))
            username, email, phone = (email_or_phone, "", email_or_phone)

        user = self.model(
            username=username,
            email=email,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        user = self._create_user(username, password, **extra_fields)
        # print(user)
        return user

    def create_staffuser(self, username, password=None, **extra_fields):
        user = self._create_user(username, password, **extra_fields)
        user.active = True
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self._create_user(username, password, **extra_fields)
        user.active = True
        user.staff = True
        user.admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='email or phone', max_length=255, unique=True, db_index=True,
        help_text='Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[validators.RegexValidator(r'^[\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid'), ],
        error_messages={'unique': "A user with that username already exists.", }
    )
    email = models.EmailField(verbose_name='email', max_length=254, blank=True)
    phone = models.CharField(verbose_name='phone', max_length=255, blank=True)
    email_verified = models.BooleanField(default=False, null=False)
    phone_verified = models.BooleanField(default=False, null=False)
    full_name = models.CharField(verbose_name='full name', max_length=1024, blank=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to='profile/%Y%m%d')
    address = models.CharField(max_length=1024, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    state = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
    

    def __str__(self):
        return self.name if self.name else str(self.pk)


class ContactUs(TimeStampedModel):
    name = models.CharField(max_length=512, blank=True, null=True)
    email = models.EmailField(max_length=216, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else str(self.pk)

    class Meta:
        ordering = ("-created_at",)


class RequestCallBack(TimeStampedModel):
    name = models.CharField(max_length=512, blank=True, null=True)
    email = models.EmailField(max_length=216, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else str(self.pk)

    class Meta:
        ordering = ("-created_at",)


class FAQ(TimeStampedModel):
    type = models.CharField(max_length=512, blank=True, null=True, choices=FAQ_TYPE)
    question = models.CharField(max_length=1024, blank=True, null=True)
    answer = models.CharField(max_length=2048, blank=True, null=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.type}->{self.question}' if self.type and self.question else str(self.pk)


class Subscription(TimeStampedModel):
    from course.models import Course
    from test_series.models import TestSeries
    from order.models import Order

    type = models.CharField(max_length=216, blank=True, null=True, choices=PRODUCT_TYPE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, blank=True, null=True)
    testseries = models.ForeignKey(TestSeries, on_delete=models.DO_NOTHING, blank=True, null=True)
    order_ref = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    validity = models.PositiveIntegerField(blank=True, null=True)
    expired_on = models.DateField(blank=True, null=True)
    expire_status = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f'subscription#{self.pk}'


class UserCourseProgress(TimeStampedModel):
    from course.models import Course, CourseSection, Lecture

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    coursesection = models.ForeignKey(CourseSection, on_delete=models.CASCADE, blank=True, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=False)
    completed_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'usercourseprogress#{self.pk}'


class UserLectureDoubt(TimeStampedModel):
    from course.models import Course, CourseSection, Lecture

    status = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=1024, blank=True, null=True)
    query = models.TextField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    coursesection = models.ForeignKey(CourseSection, on_delete=models.CASCADE, blank=True, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'doubt#{self.pk}'


class UserTestset(TimeStampedModel):
    from test_series.models import Testset, TestSeries

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    testset = models.ForeignKey(Testset, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, blank=True, null=True)
    testseries = models.ForeignKey(TestSeries, on_delete=models.CASCADE, blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    report_generated = models.CharField(max_length=512, blank=True, null=True, choices=USER_TESTSET_REPORT_STATUS)
    report_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'usertest#{self.pk}'

    def initializeUserTestsetAnswer(self, status='not_visited'):
        from account.utils import initializeUserTestsetAnswer
        return initializeUserTestsetAnswer(self, status)

    def calutateUserTestsetAnswer(self):
        from account.utils import calutateUserTestsetAnswer
        return calutateUserTestsetAnswer(self)

    def checkUserTestsetAnswer(self):
        from account.utils import checkUserTestsetAnswer
        return checkUserTestsetAnswer(self)


class UserTestsetAnswer(TimeStampedModel):
    from test_series.models import Question, Option

    user_testset = models.ForeignKey(UserTestset, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=512, blank=True, null=True, choices=QUESTION_ANSWER_STATUS)
    marks_awarded = models.FloatField(default=0, blank=True, null=True)
    selected_option_status = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    check_status = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f'usertestanswer#{self.pk}'
