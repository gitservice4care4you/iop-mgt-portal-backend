from django.contrib import admin
from city.models import City


class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "created_at", "updated_at")
    search_fields = ("name", "country")
    list_filter = ("created_at", "updated_at")

    


# Register your models here.
admin.site.register(City, CityAdmin)
