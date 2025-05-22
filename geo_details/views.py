from rest_framework import viewsets
from .models import GeoDetails
from .serializers import GeoDetailsSerializer

class GeoDetailsView(viewsets.ModelViewSet):
    queryset = GeoDetails.objects.all()
    serializer_class = GeoDetailsSerializer

