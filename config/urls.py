"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

API Authentication:
    To authenticate with the API:
    1. Use the /api/v1/token/ endpoint to get a JWT token pair
    2. In Swagger UI, click the "Authorize" button and enter your token as: "Bearer <your_token>"
    3. All authenticated endpoints will now work
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Change admin site title, header and index title
admin.site.site_header = "IOP Management Portal for Admins"
admin.site.site_title = "IOP Management Admin Panel for Admins"
admin.site.index_title = "Welcome to IOP Management "

schema_view = get_schema_view(
    openapi.Info(
        title="IOP Management API",
        default_version="v1",
        description="API documentation for IOP Management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],  # Empty list to disable default authentication
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("auth/", include("authentication.urls")),
                path("", include("user.urls")),
                path("", include("country.urls")),
                path("", include("city.urls")),
                # path("api/v1/geo-details/", include("geo_details.urls")),
                # path("api/v1/permission/", include("permission.urls")),
                # path("api/v1/role/", include("role.urls")),
                path(
                    "token/",
                    TokenObtainPairView.as_view(),
                    name="token_obtain_pair",
                ),
                path(
                    "token/refresh/",
                    TokenRefreshView.as_view(),
                    name="token_refresh",
                ),
            ]
        ),
    ),
    path(
        "doc/",
        include(
            [
                path(
                    "swagger/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="schema-swagger-ui",
                ),
                path(
                    "redoc/",
                    schema_view.with_ui("redoc", cache_timeout=0),
                    name="schema-redoc",
                ),
            ]
        ),
    ),
    path("silk/", include("silk.urls", namespace="silk")),
]
