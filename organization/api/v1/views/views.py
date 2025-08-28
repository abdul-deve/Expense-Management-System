from rest_framework.viewsets import ModelViewSet
from organization.models import Organization
from organization.api.v1.serializers.serializer import OrganizationSerializer

class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    authentication_classes = []
    permission_classes = []