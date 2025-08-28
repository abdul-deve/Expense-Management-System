from rest_framework import  serializers
from organization.models import Employee,Organization
from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model
import  requests
User = get_user_model()
class OrganizationSerializer(serializers.ModelSerializer):
    # User Data
    email = serializers.EmailField()
    # name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    #Organization Data
    class Meta:
        model = Organization
        fields = ["email","password","username","max_employee","address","type","name"]
        reads_only_fields = ["id","owner"]


    def create(self, validated_data):
        user_data = {
            "email" : validated_data.pop("email"),
            "password" : validated_data.pop("password"),
            "username" : validated_data.pop("username"),
            # "name" : validated_data.pop("name"),
       }
        response = requests.post(f"{settings.USER_AUTH_SERVICE_URL}/api/v1/auth/register/", json=user_data)
        if response.status_code not in (200, 201):
            raise serializers.ValidationError("User creation failed")

        user_info = response.json()
        user_id = user_info["id"]
        try:
            with transaction.atomic():
                user = User.objects.get(id=user_id)
                org = Organization.objects.create(admin=user, **validated_data)
            return org
        except Exception as e:
            requests.delete(f"{settings.USER_AUTH_SERVICE_URL}/api/users/{user_id}/")
            raise e






