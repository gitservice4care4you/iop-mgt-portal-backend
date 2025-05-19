from role.enums import RoleEnum
from shared.api_response import APIResponse
from rest_framework import status
from user.models import CustomUser



def is_super_admin(self, user):
    """Check if user has super admin role"""
    return str(user.groups.first()) == str(RoleEnum.SUPER_ADMIN.value)


def permission_denied_response():
    """Return standardized permission denied response"""
    return APIResponse.error(
        message="You do not have permission to perform this action.",
        status_code=status.HTTP_403_FORBIDDEN,
    )




def get_paginated_users(self, request, user_qs):
    """
    Get paginated and filtered users data

    Args:
        request: HTTP request object containing query parameters
        user_qs: Base queryset for users

    Returns:
        APIResponse: Formatted response with paginated users data
    """
    # Apply filters from filter backends
    filtered_queryset = self.filter_queryset(user_qs)
    
    # Try to paginate results
    page = self.paginate_queryset(filtered_queryset)

    if page is not None:
        # Get page size from paginator
        page_size = self.paginator.get_page_size(request)
        
        # Return paginated response
        return format_paginated_response(self, page, page_size)

    # Return non-paginated response if pagination fails
    return format_non_paginated_response(self, filtered_queryset)


def format_paginated_response(self, page, page_size):
    """
    Format paginated response with consistent structure

    Args:
        page: Paginated queryset of users
        page_size: Number of items per page

    Returns:
        APIResponse: Formatted success response with paginated data
    """
    serializer = self.get_serializer(page, many=True)
    paginated_data = self.get_paginated_response(serializer.data)

    data = {
        "users": paginated_data.data["results"],
        "total": paginated_data.data["count"],
        "next": paginated_data.data["next"],
        "previous": paginated_data.data["previous"],
        "page_size": page_size,
    }

    return APIResponse.success(
        message="Users fetched successfully",
        status_code=status.HTTP_200_OK,
        data=data,
    )


def format_non_paginated_response(self, user_qs):
    """
    Format non-paginated response with consistent structure

    Args:
        self: The view instance
        user_qs: Queryset of users

    Returns:
        APIResponse: Formatted success response with all users data
    """
    data = {
        "users": self.get_serializer(user_qs, many=True).data,
        "total": user_qs.count(),
    }

    return APIResponse.success(
        status_code=status.HTTP_200_OK,
        message="Users fetched successfully",
        data=data,
    )
