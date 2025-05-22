from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def login_with_email_doc():
    return swagger_auto_schema(
        operation_description="Login with email and password to obtain JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User email"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User password"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "status": True,
                        "message": "Login successful",
                        "data": {
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "user": {
                                "id": 1,
                                "email": "user@example.com",
                                "full_name": "John Doe",
                                "role": "Guest",
                                "country": "United States",
                                "job_title": "Software Engineer",
                                "is_active": True,
                                "is_staff": False,
                                "created_at": "2021-01-01T00:00:00Z",
                                "updated_at": "2021-01-01T00:00:00Z",
                                "groups": ["Group1", "Group2"],
                                "permissions": ["Permission1", "Permission2"],
                                "azure_id": "1234567890",
                            },
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "status": False,
                        "message": "Email and password are required",
                    }
                },
            ),
        },
    )


def login_with_azure_doc():
    return swagger_auto_schema(
        operation_description="Login with Azure AD token to obtain JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["azure_token"],
            properties={
                "azure_token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Azure AD access token"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "status": True,
                        "message": "Login successful",
                        "data": {
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "user": {
                                "id": 1,
                                "email": "user@example.com",
                                "full_name": "John Doe",
                                "role": {
                                    "id": 1,
                                    "name": "Guest",
                                    "description": "Guest role",
                                },
                                "country": {
                                    "id": 1,
                                    "name": "United States",
                                    "code": "US",
                                    "description": "United States",
                                },
                                "job_title": "Software Engineer",
                                "is_active": True,
                                "is_staff": False,
                                "created_at": "2021-01-01T00:00:00Z",
                                "updated_at": "2021-01-01T00:00:00Z",
                                "groups": ["Group1", "Group2"],
                                "permissions": ["Permission1", "Permission2"],
                                "azure_id": "1234567890",
                                "photo": "https://example.com/photo.jpg",
                            },
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "status": False,
                        "message": "Azure token is required",
                    }
                },
            ),
        },
    )


def token_refresh_doc():
    return swagger_auto_schema(
        operation_description="Refresh JWT token using refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING, description="JWT refresh token"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Token refreshed successfully",
                examples={
                    "application/json": {
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    }
                },
            ),
            401: openapi.Response(
                description="Invalid refresh token",
                examples={
                    "application/json": {
                        "detail": "Token is invalid or expired",
                        "code": "token_not_valid",
                    }
                },
            ),
        },
    )


def token_blacklist_doc():
    return swagger_auto_schema(
        operation_description="Logout by blacklisting the refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="JWT refresh token to blacklist",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Token blacklisted successfully",
                examples={
                    "application/json": {"status": True, "message": "Logout successful"}
                },
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "detail": "Token is invalid or expired",
                        "code": "token_not_valid",
                    }
                },
            ),
        },
    )
