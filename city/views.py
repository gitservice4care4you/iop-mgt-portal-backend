from django.shortcuts import render
from rest_framework import viewsets
from city.models import City
from city.serializers import CitySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# Create your views here.
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    ordering_fields = ["name", "country__name"]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ["name", "country__name"]
