from django.db import models
from city.models import City


# Create your models here.
class GeoDetails(models.Model):
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    map_url = models.URLField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Geo Details"
        verbose_name_plural = "Geo Details"

    def __str__(self):
        return self.description
