from django.urls import include, path
from .views import PermissionViewSet, UserViewSet, GroupViewSet
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # path("", include(router.urls)),
]

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("permissions", PermissionViewSet, basename="permission")
router.register("groups", GroupViewSet, basename="group")
urlpatterns += router.urls
