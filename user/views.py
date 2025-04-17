from django.shortcuts import render
from rest_framework import viewsets
from role.enums import RoleEnum
from user.filters import UserFilter
from user.models import CustomUser
from user.serializers import (
    UserActivateSerializer,
    UserSerializer,
    PermissionSerializer,
    GroupSerializer,
)
from django.contrib.auth.models import Permission, Group
from rest_framework.permissions import AllowAny, IsAuthenticated
from shared.api_response import APIResponse
from rest_framework import status, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from user.services import (
    get_paginated_users,
    is_super_admin,
    permission_denied_response,
)
from .swagger import list_doc


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    User management endpoints.

    list:
        Retrieve a list of users with filtering, ordering and search capabilities.

        Filters:
            - email: Filter by email address
              Example: ?email=user@example.com

            - role: Filter by role ID
              Example: ?role=1 (Admin), ?role=2 (Manager)

            - country: Filter by country ID
              Example: ?country=1 (USA), ?country=2 (Canada)

            - is_active: Filter by active status
              Example: ?is_active=true or ?is_active=false

            - is_staff: Filter by staff status
              Example: ?is_staff=true or ?is_staff=false

            - created_at: Filter by creation date
              Example: ?created_at=2023-01-01

            - updated_at: Filter by last update date
              Example: ?updated_at=2023-01-01

        Ordering:
        - fullname: Order by full name
        - email: Order by email
        - is_active: Order by active status
        - is_staff: Order by staff status
        - role: Order by role
        - country: Order by country
        - created_at: Order by creation date

        Add '-' prefix for descending order, e.g. '-created_at'

        Search:
        - Searches across fullname and email fields

        Pagination:
        - Page size: 10 items per page
        - Use page parameter to navigate pages

    create:
        Create a new user.

    retrieve:
        Get details of a specific user.

    update:
        Update all fields of an existing user.

    partial_update:
        Update specific fields of an existing user.

    destroy:
        Delete a user.
    """

    # ---------------------------------------------------------------------------- #
    #                                main variables                                #
    # ---------------------------------------------------------------------------- #
    queryset = CustomUser.objects.all()
    # serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filterset_class = UserFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = [
        "full_name",
        "email",
        "is_active",
        "is_staff",
        "role",
        "country",
        "created_at",
    ]
    search_fields = ["full_name", "email"]
    list_doc = list_doc()
    # ---------------------------------------------------------------------------- #
    #                            override generic method                           #
    # ---------------------------------------------------------------------------- #

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["activate", "deactivate"]:
            return UserActivateSerializer
        return UserSerializer

    class CustomPagination(PageNumberPagination):
        page_size_query_param = "page_size"

    # ---------------------------------------------------------------------------- #
    #                                   Main APIs                                  #
    # ---------------------------------------------------------------------------- #

    @list_doc
    def list(self, request, *args, **kwargs):

        # Check if user has super admin permissions
        is_admin = is_super_admin(self, user=request.user)

        if not is_admin:
            return permission_denied_response()

        # Get and process users with pagination
        return get_paginated_users(self, request=request, user_qs=self.queryset)

    # ---------------------------------------------------------------------------- #
    #                                   Profile                                #
    # ---------------------------------------------------------------------------- #

    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        return APIResponse.success(
            message="User account fetched successfully",
            status_code=status.HTTP_200_OK,
            data=self.get_serializer(user).data,
        )

    # ---------------------------------------------------------------------------- #
    #                                  activation                                  #
    # ---------------------------------------------------------------------------- #

    @action(detail=False, methods=["post"])
    def activate(self, request, *args, **kwargs):
        try:
            # Check if user is trying to deactivate their own account
            if request.user.id == request.data.get("id"):
                return APIResponse.error(
                    message="You cannot activate your own account",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Get user data from request body and validate with serializer
            user = None
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return APIResponse.error(
                    message="Invalid user data",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            # Get user ID from validated data
            user_id = serializer.validated_data.get("id")
            if user_id == "":
                return APIResponse.error(
                    message="User ID is required",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Check if user exists
            try:

                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return APIResponse.error(
                    message="User not found", status_code=status.HTTP_404_NOT_FOUND
                )

            if user.id == request.user.id:
                return APIResponse.error(
                    message="You cannot activate your own account",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Check if user is already active
            if user.is_active:
                return APIResponse.success(
                    message="User is already activated",
                    status_code=status.HTTP_200_OK,
                )

            # Activate user
            user.is_active = True
            user.save()

            return APIResponse.success(
                message="User activated successfully", status_code=status.HTTP_200_OK
            )

        except Exception as e:
            return APIResponse.error(
                message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def deactivate(self, request, *args, **kwargs):
        try:
            # Check if user is trying to deactivate their own account
            if request.user.id == request.data.get("id"):
                return APIResponse.error(
                    message="You cannot deactivate your own account",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Get user ID from request body
            user_id = request.data.get("id")
            if not user_id:
                return APIResponse.error(
                    message="User ID is required",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Check if user exists
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return APIResponse.error(
                    message="User not found", status_code=status.HTTP_404_NOT_FOUND
                )

            # Check if user is already active
            if not user.is_active:
                return APIResponse.success(
                    message="User is already deactivated",
                    status_code=status.HTTP_200_OK,
                )

            # Activate user
            user.is_active = False
            user.save()

            return APIResponse.success(
                message="User deactivated successfully", status_code=status.HTTP_200_OK
            )

        except Exception as e:
            return APIResponse.error(
                message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        permissions = Permission.objects.all()
        is_admin = request.user.role and (
            request.user.role.name == "super_admin"
            or request.user.role.name == "portal_admin"
        )
        if is_admin:
            return APIResponse.success(
                message="Permission list fetched successfully",
                status_code=status.HTTP_200_OK,
                data=self.serializer_class(permissions, many=True).data,
            )
        else:
            return APIResponse.error(
                message="You do not have permission to perform this action.",
                status_code=status.HTTP_403_FORBIDDEN,
            )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
