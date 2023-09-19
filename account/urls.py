from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from account.views.api import (
    AskDoubtview,
    Profile,
    SendOTP,
    VerifyOTP,
    ContactUsView,
    RequestCallBackView,
    MySubscriptionView,
    AdminLogin
)

api_urlpatterns = [
    #admin login
    path('account/admin/login', AdminLogin.as_view(), name="admin_login"),
    
    path('account/profile', Profile.as_view(), name='profile'),

    # send, resend , verify otp and refresh token
    path('account/send-otp', SendOTP.as_view(), name="send_otp"),
    path('account/resend-otp', SendOTP.as_view(), name="re_send_otp"),
    path('account/verify-otp', VerifyOTP.as_view(), name="verify_otp"),
    path('account/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # user query, call back request
    path('contact_us', ContactUsView.as_view(), name="contact_us"),
    path('request_callback', RequestCallBackView.as_view(), name="contact_us"),
    path('lecture/askdoubt', AskDoubtview.as_view(), name='lecture_ask_doubt'),


    # subscription
    path('mysubscription', MySubscriptionView.as_view(), name='my_subscription'),
]

urlpatterns = api_urlpatterns
