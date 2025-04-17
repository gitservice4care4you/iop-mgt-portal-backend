from django.contrib import admin
from role.models import Role


# Register your models here.
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "updated_at", "created_at")
    search_fields = ("name", "description")
    list_filter = ("name", "description")




admin.site.register(Role, RoleAdmin)
