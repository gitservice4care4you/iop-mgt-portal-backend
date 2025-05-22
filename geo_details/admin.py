from django.contrib import admin

from geo_details.models import GeoDetails


class GeoDetailsAdmin(admin.ModelAdmin):
    list_display = ("description", "latitude", "longitude", "city", "created_at", "updated_at")
    search_fields = ("description", "city__name")
    list_filter = ("created_at", "updated_at", "city")

    verbose_name = "Geo Details"
    verbose_name_plural = "Geo Details"


# Register your models here.
admin.site.register(GeoDetails, GeoDetailsAdmin)
