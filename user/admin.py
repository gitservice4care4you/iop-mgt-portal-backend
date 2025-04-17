from django.contrib import admin
from .models import CustomUser

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "role", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("role", "is_active", "is_staff")

    verbose_name = "User"
    verbose_name_plural = "Users"


admin.site.register(CustomUser, UserAdmin)
