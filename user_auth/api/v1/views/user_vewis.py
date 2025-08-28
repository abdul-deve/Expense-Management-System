from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework import status
from dj_rest_auth.registration.views import ConfirmEmailView as BaseConfirmEmailView
from rest_framework.permissions import AllowAny


from user_auth.api.v1.serializers.user_serializer import RegisterSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed




User = get_user_model()
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),

    }
class RegisterAPI(CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={"context":request})
        if  serializer.is_valid(raise_exception=True):
            data = {
                "Username" : request.data["username"],
                "message" : "Check your email to  Register account"
            }
            user = serializer.save()
            user.is_active= False
            user.save()
            return Response(data=data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class ConfirmEmailView(BaseConfirmEmailView):
    def get(self, *args, **kwargs):
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({"detail": "Email confirmed successfully"}, status=status.HTTP_200_OK)
