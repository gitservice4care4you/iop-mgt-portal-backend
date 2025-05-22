from django.contrib import admin

from country.models import Country

# Register your models here.


class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at", "updated_at")
    search_fields = ("name", "code")
    list_filter = ("created_at", "updated_at")

    verbose_name = "Country"
    verbose_name_plural = "Countries"


admin.site.register(Country, CountryAdmin)
