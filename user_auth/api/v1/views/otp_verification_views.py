from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from user_auth.api.v1.serializers.otp_serializer import SendOTPSerializer, VerifyOTPSerializer
from rest_framework.permissions import AllowAny

User = get_user_model()

class SendOTPAPI(CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = SendOTPSerializer
    def create(self, request,*args,**kwargs):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email") or request.user.email
        user = User.objects.get(email=email)
        try:
            result = user.set_send_otp()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPAPI(CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer
    def create(self, request,*args,**kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data["otp"]
        email = serializer.validated_data.get("email")

        try:
            user = request.user if request.user.is_authenticated else User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = user.verify_otp(otp)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


