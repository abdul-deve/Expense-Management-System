from django.urls import path, include

app_name = 'user_auth'

urlpatterns = [
    path('v1/', include('user_auth.api.v1.urls')),
]