from shared.api_response import APIResponse
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from user.models import CustomUser
from authentication.serializers import CustomTokenObtainPairSerializer, UserSerializer


class AuthenticationService:
    user_serializer = UserSerializer

    def __init__(self):
        pass

    def validate_credentials(self, email: any, password: any):
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
    def get_user(self, email: str) -> CustomUser:
        """Get user by email if exists"""
        try:
            return CustomUser.objects.prefetch_related("groups", "role", "country").get(
                email=email
            )
        except CustomUser.DoesNotExist:
            return None

    # --------------------------- generate token pair --------------------------- #
    def generate_token_response(self, user: CustomUser):
        """Generate token pair and user data response"""
        token = CustomTokenObtainPairSerializer.get_token(user)

        return token

    # --------------------------- generate success response --------------------------- #
    def generate_success_response(self, token: any, user: any):
        """Generate success response"""
        user_data = self.user_serializer(user).data
        data = {
            "token": {
                "refresh": str(token.access_token),
                "access": str(token),
                "expires_in": token.access_token.lifetime.total_seconds() // 60,
                # "expires_at": token.access_token.expires_at,
            },
            "user": user_data,
        }
        return APIResponse.success(
            data=data,
            message="User data fetched successfully",
            status_code=HTTP_200_OK,
        )
