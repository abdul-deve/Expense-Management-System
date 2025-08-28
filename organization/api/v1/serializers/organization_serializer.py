from rest_framework import serializers
from django.contrib.auth import get_user_model
from organization.models import Organization, PendingOrganization
from user_auth.api.v1.serializers.user_serializer import RegisterSerializer

User = get_user_model()

class OrganizationCreateSerializer(serializers.Serializer):
    """
    Comprehensive serializer for creating user + organization in one API call
    """
    # User data
    username = serializers.CharField(max_length=250)
    name = serializers.CharField(max_length=250)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    # Organization data
    org_name = serializers.CharField(max_length=255)
    org_description = serializers.CharField(required=False, allow_blank=True, default="")
    org_type = serializers.ChoiceField(choices=Organization.ORG_TYPES)
    org_address = serializers.CharField(max_length=50)
    org_max_employee = serializers.IntegerField(min_value=1)
    
    def validate_email(self, value):
        """Check if email is already taken"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        """Check if username is already taken"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def validate_org_name(self, value):
        """Check if organization name is already taken"""
        if Organization.objects.filter(name=value).exists():
            raise serializers.ValidationError("An organization with this name already exists.")
        return value

class OrganizationDetailSerializer(serializers.ModelSerializer):
    """Serializer for returning organization details with owner info"""
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    current_employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'type', 'address', 'num_of_employee', 
            'max_employee', 'current_employee_count', 'created_at',
            'owner_name', 'owner_email', 'owner_username'
        ]
    
    def get_current_employee_count(self, obj):
        return obj.current_employee_count()

class PendingOrganizationSerializer(serializers.ModelSerializer):
    """Serializer for pending organization data"""
    class Meta:
        model = PendingOrganization
        fields = ['id', 'org_name', 'org_description', 'admin_email', 'status', 'created_at']















