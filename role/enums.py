from django.utils.translation import gettext_lazy as _
from django.db import models


class RoleEnum(models.TextChoices):
    SUPER_ADMIN = "Super Admin", _("Super Admin")
    PORTAL_ADMIN = "Portal Admin", _("Portal Admin")
    MODERATOR = "Moderator", _("Moderator")
    RESEARCHER = "Researcher", _("Researcher")
    COUNTRY_MANAGER = "Country Manager", _("Country Manager")
    REPORTER = "Reporter", _("Reporter")
    GUEST = "Guest", _("Guest")

    def __str__(self):
        return self.value
