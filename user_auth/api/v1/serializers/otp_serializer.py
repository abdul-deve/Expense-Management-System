from rest_framework import serializers

from rest_framework import serializers

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True,allow_blank=True)
    otp = serializers.CharField(max_length=6,allow_null=False,allow_blank=False)

    def create(self, validated_data):
        return super().create

    def update(self, instance, validated_data):
        return super().update

