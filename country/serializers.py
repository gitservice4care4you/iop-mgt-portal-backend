from rest_framework import serializers
from city.models import City
from city.serializers import CitySerializer
from country.models import Country


class CountrySerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "code",
            "cities",
            "created_at",
            "updated_at",
        )

    def get_cities(self, obj):
        cities = City.objects.filter(country=obj)
        return CitySerializer(cities, many=True).data
