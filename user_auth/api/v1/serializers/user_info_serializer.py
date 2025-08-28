from rest_framework import serializers
from django.contrib.auth import get_user_model

from user_auth.models import UserProfile,Address

User = get_user_model()

class UserInfoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserProfile
        # fields = ["user","phone_number","profile_pic","created_at","updated_at"]
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["created_at","updated_at"]


