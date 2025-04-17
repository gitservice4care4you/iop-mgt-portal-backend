from django.urls import path
from role.views import RoleViewSet

urlpatterns = [
    path("roles/", RoleViewSet.as_view(), name="role-list"),
]
