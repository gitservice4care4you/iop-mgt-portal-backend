from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework.status import *
from authentication.serializers import CustomTokenObtainPairSerializer
from role.models import Role
from shared.api_response import APIResponse
from user.models import CustomUser
from user.serializers import UserSerializer
from rest_framework.permissions import AllowAny


class CustomTokenObtainPairView(TokenObtainPairView):
    """View for obtaining JWT tokens with custom claims"""

    serializer_class = CustomTokenObtainPairSerializer
    user_serializer = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Handle POST request to obtain tokens"""
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            # Validate that email and password are provided in the request
            self._validate_credentials(email, password)

            # Get user by email if exists
            user = self._get_user(email)

            if user != None:
                # if user exists, generate token and return success response
                token = self._generate_token_response(user)
                return self._generate_success_response(token, user)
            else:
                # if user does not exist, create an account for the user with minimum permissions
                try:
                    new_user = CustomUser.objects.create_user(
                        email=email,
                        password=password,
                        is_active=True,
                        role=Role.objects.get(name="Guest"),
                    )
                    token = self._generate_token_response(new_user)
                    return self._generate_success_response(token, new_user)
                except Exception as e:
                    return APIResponse.error(
                        message=str(e), status_code=HTTP_400_BAD_REQUEST
                    )

        except Exception as e:
            return APIResponse.error(message=str(e), status_code=HTTP_400_BAD_REQUEST)

    # ---------------------------------------------------------------------------- #
    #                                 class methods                                #
    # ---------------------------------------------------------------------------- #

    # --------------------------- validate credentials --------------------------- #
    def _validate_credentials(self, email: any, password: any):
        """Validate that both email and password are provided"""
        if email == "" or email is None:
            return APIResponse.error(
                message="Email is required", status_code=HTTP_400_BAD_REQUEST
            )
        if password == "" or password is None:
            return APIResponse.error(
                message="Password is required", status_code=HTTP_400_BAD_REQUEST
            )
        return

    # --------------------------- get user by email --------------------------- #
    def _get_user(self, email: str) -> CustomUser:
        """Get user by email if exists"""
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    # --------------------------- generate token pair --------------------------- #
    def _generate_token_response(self, user: CustomUser):
        """Generate token pair and user data response"""
        token = CustomTokenObtainPairSerializer.get_token(user)

        return token

    # --------------------------- generate success response --------------------------- #
    def _generate_success_response(self, token: any, user: any):
        """Generate success response"""
        user_data = self.user_serializer(user).data
        data = {
            "token": {
                "refresh": str(token.access_token),
                "access": str(token),
            },
            "user": user_data,
        }
        return APIResponse.success(
            data=data,
            message="User data fetched successfully",
            status_code=HTTP_200_OK,
        )
