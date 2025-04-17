from django.contrib import admin

from permission.models import Permission


class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")

    verbose_name = "Permission"
    verbose_name_plural = "Permissions"


# Register your models here.

admin.site.register(Permission, PermissionAdmin)
