from django.urls import path
from country.views import CountryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"countries", CountryViewSet, basename="country")

urlpatterns = router.urls
