from django.shortcuts import render
from rest_framework import viewsets
from city.models import City
from city.serializers import CitySerializer


# Create your views here.
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
