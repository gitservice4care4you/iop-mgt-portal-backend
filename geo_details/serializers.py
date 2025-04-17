from .models import GeoDetails
from rest_framework import serializers

class GeoDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoDetails
        fields = '__all__'
