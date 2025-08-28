from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from user_auth.api.v1.views.user_info_views import AddressViewSet, UserProfileViewSet
from user_auth.api.v1.views.otp_verification_views import SendOTPAPI, VerifyOTPAPI
from user_auth.api.v1.views.user_vewis import RegisterAPI

router = DefaultRouter()
router.register('profile', UserProfileViewSet, basename='profile')
router.register('address', AddressViewSet, basename='address')

urlpatterns = [
    #JWT endpoints
    path('register/', RegisterAPI.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # OTP Verification
    path("otp/send/", SendOTPAPI.as_view(), name="send-otp"),
    path("otp/verify/", VerifyOTPAPI.as_view(), name="verify-otp"),
    path("otp/resend/", SendOTPAPI.as_view(), name="resend-otp"),

    # User profiles and addresses
    path('', include(router.urls)),
    path('', include('dj_rest_auth.urls')),
    # path('registration/', include('dj_rest_auth.registration.urls')),
    # path('registration/confirm-email/', ConfirmEmailView.as_view(), name='rest_confirm'),
]