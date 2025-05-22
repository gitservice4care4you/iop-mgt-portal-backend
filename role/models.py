from django.db import models
from django.utils.translation import gettext_lazy as _
from role.enums import RoleEnum


# Create your models here.
class Role(models.Model):
    name = models.CharField(
        max_length=255, unique=True, choices=RoleEnum.choices, default=RoleEnum.GUEST
    )
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
