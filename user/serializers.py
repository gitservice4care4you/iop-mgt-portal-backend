from rest_framework import serializers
from role.serializers import RoleSerializer
from user.models import CustomUser
from django.contrib.auth.models import Permission, Group


class PermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(slug_field="model", read_only=True)

    class Meta:
        model = Permission
        fields = ["id", "codename", "name", "content_type"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "is_active",
            "is_staff",
            "job_title",
            "country",
            "groups",
            "created_at",
            "updated_at",
        ]


class UserActivateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ["id"]
