from rest_framework import serializers
from django.contrib.auth import authenticate
from user_auth.models import User



class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password', 'name','username')

    def validate(self, data):
        if data["password"] != data.pop("confirm_password"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "name": self.validated_data.get("name", ""),
            "email": self.validated_data.get("email", ""),
            "password": self.validated_data.get("password", ""),
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_send_otp()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=250, allow_null=False, allow_blank=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        attrs['user'] = user
        return attrs
