from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from api_rest.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api_rest.urls'), name='api_rest_urls'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
