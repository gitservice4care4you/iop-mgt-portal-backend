from rest_framework.routers import DefaultRouter
from city.views import CityViewSet

router = DefaultRouter()
router.register(r"cities", CityViewSet, basename="city")

urlpatterns = router.urls
