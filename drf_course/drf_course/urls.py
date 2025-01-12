
from django.contrib import admin
from django.urls import path ,include
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView , SpectacularRedocView ,SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('silk/', include('silk.urls' , namespace='silk')),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/Schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/Schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-url"),
    path("api/token/redoc/", SpectacularRedocView.as_view(url_name="redoc") , name= 'redoc'),


]
