from django.urls import path, include

app_name = 'organization'

urlpatterns = [
    path('v1/', include('organization.api.v1.urls')),
]