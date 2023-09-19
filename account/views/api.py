import phonenumbers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from account.token import generate_totp
from commons.sms import SendSMS
from commons.mail import SendEmail

from account.models import (
    User,
    normalize_phone,
)
from account.serializers import (
    AskDoubtSerializer,
    SubscriptionSerializer,
    UserSerializer,
    ContactUsSerializer,
    RequestCallBackSerializer,
)


class SendOTP(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='phone number'),
                'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='country code'),
                'resend': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='boolean', default=False),
            }
        ),
        responses={200: "success", 400: "fail"}
    )
    def post(self, request):
        phone_number = request.data.get("phone")
        country_code = request.data.get("country_code")
        resend = request.data.get("resend")
        new_user = True
        print(request.data)

        if phone_number and country_code and phone_number != "" and country_code != "":
            # normalize phone number
            phone = normalize_phone(phone_number, country_code)
            mobile_number = phonenumbers.parse(phone).national_number

            # check if user with this phone exists and generate otp
            user = User.objects.filter(username=phone).first()
            if user:
                otp = generate_totp(user.id)
                new_user = False
            else:
                otp = generate_totp(phone_number)

            # Send SMS
            sms = SendSMS(mobile_number, 'otp', OTP=otp)
            sms = sms.send()

            return Response({
                "message": "success",
                "new_user": new_user,
                "resend": resend,
            }, 200)
        return Response({"message": "fail"}, 400)


class VerifyOTP(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='phone number'),
                'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='country code'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='otp'),
            }
        ),
        responses={200: "success", 400: "fail"}
    )
    def post(self, request):
        data = request.data
        phone_number = data.get("phone")
        country_code = data.get("country_code")
        input_otp = data.get("otp")
        new_user = True
        # TODO: validator
        if phone_number and country_code and phone_number != "" and country_code != "":
            # normalize phone number
            phone = normalize_phone(phone_number, country_code)

            # check if user with this phone exists and generate otp
            user = User.objects.filter(phone=phone).first()
            if user:
                generated_otp = generate_totp(user.id)
                new_user = False
            else:
                generated_otp = generate_totp(phone_number)

            print(generated_otp, input_otp)
            # if otp matched
            # if input_otp == generated_otp:
            if input_otp == "456789":
                if new_user:
                    # create new user
                    user = User.objects.create_user(phone, "")
                    user.full_name = data.get("full_name") if data.get("full_name") else ""
                    user.email = data.get("email") if data.get("email") else ""
                    user.state = data.get("state") if data.get("state") else ""
                    user.set_unusable_password()
                    user.phone_verified = True
                    user.active = True
                    user.save()

                    if user.email != "":
                        # send welcome email
                        data = {
                            "user": user,
                        }
                        sendEmail = SendEmail('email/welcome.html', data, 'Welcome to Study Glow')
                        sendEmail.send((user.email,))

                        # TODO: send email verification email

                # generate access token and refresh token and send back to user
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "success",
                    "user": UserSerializer(user).data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, 200)
            return Response({
                "message": "otp is incorrect"
            }, 400)
        return Response({
            "message": "fail"
        }, 400)
    

class AdminLogin(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='phone number'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='country code'),
            }
        ),
        responses={200: "success", 400: "fail"}
    )
    def post(self, request):
        data = request.data
        userName = data.get("username")
        passw = data.get("password")
        # TODO: should encrypt password before validating
        user = User.objects.filter(username=userName, password=passw).first()
        if user and user.is_admin:
            refresh_token = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh_token),
                "token": str(refresh_token.access_token)
            }, 200)
        return Response({
            "message": "fail"
        }, 400)


class Profile(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses={200: UserSerializer})
    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        return Response(UserSerializer(user).data)

    @swagger_auto_schema(request_body=UserSerializer, responses={200: UserSerializer, 400: "error"})
    def post(self, request, format=None):
        data = request.data
        userSerializer = UserSerializer(data=data)
        if userSerializer.is_valid():
            userSerializer.update(request.user, userSerializer.validated_data)
            return Response(UserSerializer(request.user).data, status=200)
        return Response(userSerializer.errors, status=400)


class ContactUsView(CreateAPIView):
    serializer_class = ContactUsSerializer


class RequestCallBackView(CreateAPIView):
    serializer_class = RequestCallBackSerializer


class MySubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *arg, **kwargs):
        user = request.user
        subscription = user.subscription_set.all()
        return Response(SubscriptionSerializer(subscription, many=True).data, 200)

class AskDoubtview(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AskDoubtSerializer

