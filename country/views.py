from django.shortcuts import render
from rest_framework import viewsets

from city.serializers import CitySerializer
from country.filters import CountryFilter
from country.paginations import CountryPagination
from shared.api_response import APIResponse
from user.paginations import CustomPagination
from .models import Country
from .serializers import CountrySerializer
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from .swagger import list_doc


# Create your views here.
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CountryPagination
    filterset_class = CountryFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["name", "code"]
    search_fields = ["name", "code"]
    list_doc = list_doc()

    @list_doc
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        fetched_data = {
            "total": data["count"],
            "next": data["next"],
            "previous": data["previous"],
            "page_size": self.pagination_class.page_size,
            "countries": data["results"],
        }

        return APIResponse.success(
            message="Country fetched successfully",
            status_code=status.HTTP_200_OK,
            data=data,
        )
