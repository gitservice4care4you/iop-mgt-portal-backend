from django.urls import path
from city.views import CityViewSet

urlpatterns = [
    path("cities/", CityViewSet.as_view(), name="city-list"),
]
