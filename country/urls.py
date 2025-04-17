from django.urls import path
from country.views import CountryViewSet

urlpatterns = [
    path("countries/", CountryViewSet.as_view(), name="country-list"),
]
