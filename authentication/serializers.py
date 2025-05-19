from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import CustomUser
from user.serializers import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        
        # Add custom claims
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["id"] = str(user.id)
        token["is_superuser"] = user.is_superuser
        token["is_staff"] = user.is_staff
        token["is_active"] = user.is_active

        # Handle role - could be None or need string conversion if it's a UUID
        if user.role:
            token["role"] = str(user.role.id)
        else:
            token["role"] = None

        # Handle country - could be None or need string conversion if it's a UUID
        if user.country:
            token["country"] = str(user.country.id)
        else:
            token["country"] = None

        return token

    class Meta:
        model = CustomUser
        fields = ["email", "password"]
