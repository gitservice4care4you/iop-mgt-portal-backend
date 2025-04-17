from django.contrib import admin
from .models import CustomUser

# Register your models here.


class UserAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "full_name",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
    )
    search_fields = ("email", "full_name", "first_name", "last_name")
    list_filter = ("role", "country", "full_name", "is_active", "is_staff")
    list_per_page = 10
    verbose_name = "User"
    verbose_name_plural = "Users"


admin.site.register(CustomUser, UserAdmin)
