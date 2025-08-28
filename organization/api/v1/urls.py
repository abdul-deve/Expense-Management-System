from django.urls import path, include
from .views.views import OrganizationViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("organization", OrganizationViewSet, "org")

urlpatterns = [
]
    # New comprehensive organization endpoints
