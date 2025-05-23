from rest_framework import serializers
from city.models import City


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "country",
            "created_at",
            "updated_at",
        ]
