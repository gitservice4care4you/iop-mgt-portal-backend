from django.shortcuts import render
from rest_framework import viewsets
from role.enums import RoleEnum
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
from rest_framework import status
from rest_framework.decorators import action


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    # serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # ---------------------------------------------------------------------------- #
    #                              Serializer Classes                              #
    # ---------------------------------------------------------------------------- #

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["activate", "deactivate"]:
            return UserActivateSerializer
        return UserSerializer

    # ---------------------------------------------------------------------------- #
    #                                   Main                                       #
    # ---------------------------------------------------------------------------- #

    def list(self, request, *args, **kwargs):
        user_group = str(request.user.groups.first()) == str(RoleEnum.SUPER_ADMIN.value)

        is_admin = request.user.role and (
            request.user.role.name == "super_admin"
            or request.user.role.name == "portal_admin"
        )
        if user_group:
            users = CustomUser.objects.all()
            return APIResponse.success(
                data=self.get_serializer(users, many=True).data,
                message="User list fetched successfully",
                status_code=status.HTTP_200_OK,
            )
        else:
            return APIResponse.error(
                message="You do not have permission to perform this action.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

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
