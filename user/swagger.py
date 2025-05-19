from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def list_doc():
    return swagger_auto_schema(
        operation_description="Get filtered & paginated list of users",
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by email (icontains)",
            ),
            openapi.Parameter(
                "country",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by country (icontains)",
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Pagination page number",
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Number of results per page (default: 10, max: 100)",
            ),
            openapi.Parameter(
                "ordering",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Order results by field. Options: full_name, email, is_active, is_staff, role__name, country__name, groups__name, created_at. Use '-' prefix for descending order (e.g. -created_at). Multiple fields can be used with comma separator (e.g. role__name,-created_at).",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Paginated and filtered users",
                examples={
                    "application/json": {
                        "status": True,
                        "message": "Fetched successfully",
                        "data": {
                            "count": 20,
                            "next": "/api/users/?page=2",
                            "previous": None,
                            "results": [{"id": 1, "username": "admin"}],
                        },
                    }
                },
            ),
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {
                        "status": False,
                        "message": "You do not have permission to perform this action.",
                    }
                },
            ),
        },
    )
