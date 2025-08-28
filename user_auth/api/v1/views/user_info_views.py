# user/views.py
from rest_framework import viewsets, permissions
from user_auth.models import UserProfile, Address
from user_auth.api.v1.serializers.user_info_serializer import UserInfoSerializer,AddressSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserInfoSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = []
    authentication_classes = []

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #
    # def get_queryset(self):
    #     return UserProfile.objects.filter(user=self.request.user)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = []
    authentication_classes = []

    # def perform_create(self, serializer):
    #
    #     profile = getattr(self.request.user, 'user_profile', None)
    #     if profile is None:
    #         raise serializer.ValidationError("UserProfile does not exist.")
    #     serializer.save(user=profile)
    #
    # def get_queryset(self):
    #     profile = getattr(self.request.user, 'user_profile', None)
    #     if profile is None:
    #         return Address.objects.none()
    #     return Address.objects.filter(user=profile)
