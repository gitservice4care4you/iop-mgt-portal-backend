import os
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework.status import *
from authentication.azure_service import AzureService
from authentication.serializers import CustomTokenObtainPairSerializer
from authentication.services import AuthenticationService
from role.models import Role
from shared.api_response import APIResponse
from user.models import CustomUser
from user.serializers import UserSerializer
from rest_framework.permissions import AllowAny
import requests
import jwt
from rest_framework.decorators import action
from rest_framework.views import APIView
from authentication.swagger import login_with_email_doc, login_with_azure_doc
from django.contrib.auth.models import Group


class CustomTokenObtainPairView(TokenObtainPairView):
    """View for obtaining JWT tokens with custom claims"""

    serializer_class = CustomTokenObtainPairSerializer
    user_serializer = UserSerializer
    permission_classes = [AllowAny]
    authentication_service = AuthenticationService()
    JWKS_URL = "https://login.microsoftonline.com/common/discovery/v2.0/keys"
    AUDIENCE = os.environ.get("AZURE_AD_CLIENT_ID")
    ISSUER = (
        f"https://login.microsoftonline.com/{os.environ.get('AZURE_AD_TENANT_ID')}/v2.0"
    )

    @login_with_email_doc()
    def post(self, request, *args, **kwargs):
        """Handle POST request to obtain tokens"""
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            # Validate that email and password are provided in the request
            self.authentication_service.validate_credentials(email, password)

            # Get user by email if exists
            user = self.authentication_service.get_user(email)

            if user != None:
                # if user exists, generate token and return success response
                token = self.authentication_service.generate_token_response(user)
                return self.authentication_service.generate_success_response(
                    token, user
                )
            else:
                # if user does not exist, create an account for the user with minimum permissions
                try:
                    new_user = CustomUser.objects.create_user(
                        email=email,
                        password=password,
                        is_active=True,
                        role=Role.objects.get(name="Guest"),
                    )
                    token = self.authentication_service.generate_token_response(
                        new_user
                    )
                    return self.authentication_service.generate_success_response(
                        token, new_user
                    )
                except Exception as e:
                    return APIResponse.error(
                        message=str(e), status_code=HTTP_400_BAD_REQUEST
                    )

        except Exception as e:
            return APIResponse.error(message=str(e), status_code=HTTP_400_BAD_REQUEST)


class CustomLoginWithAzureView(APIView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    azure_service = AzureService()
    authentication_service = AuthenticationService()

    @login_with_azure_doc()
    def post(self, request, *args, **kwargs):
        # try:

        # Get token from Authorization header
        azure_token = request.data.get("azure_token")
        if not azure_token:
            return APIResponse.error(
                message="Azure token is required",
                status_code=HTTP_400_BAD_REQUEST,
            )

        # Get user data from MS GRAPH API
        azure_user = self.azure_service.get_user_profile(azure_access_token=azure_token)
        # Check if user data is not empty
        if not azure_user:
            return APIResponse.error(
                message="Failed to retrieve user data from Azure",
                status_code=HTTP_400_BAD_REQUEST,
            )
        print(f"azure_user: {azure_user}")
        # check if user exists in database
        user = CustomUser.objects.filter(email=azure_user["mail"].lower()).first()
        if user:
            # if user exists, generate token and return success response
            token = self.authentication_service.generate_token_response(user)
            return self.authentication_service.generate_success_response(token, user)
            # if user does not exist, create an account for the user with minimum permissions
        try:
            user_data = self.azure_service.get_user_from_json(azure_user=azure_user)
            photo = self.azure_service.get_user_photo(azure_access_token=azure_token)
            new_user = CustomUser.objects.create_user(
                is_active=True,
                role=Role.objects.get(name="Guest"),
                photo=photo,
                **user_data,
            )
            # Assign user to "Guests" group
            guests_group, created = Group.objects.get_or_create(name="Guests")
            new_user.groups.add(guests_group),
            
            new_user.save()
            token = self.authentication_service.generate_token_response(new_user)
            return self.authentication_service.generate_success_response(
                token, new_user
            )
        except Exception as e:
            return APIResponse.error(
                message=f"Failed to create user: {str(e)}",
                status_code=HTTP_400_BAD_REQUEST,
            )

    # except Exception as e:
    #     return APIResponse.error(
    #         message=f"Failed to login with Azure: {str(e)}",
    #         status_code=HTTP_400_BAD_REQUEST,
    #     )
