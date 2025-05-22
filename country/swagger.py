from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def list_doc():
    """
    Swagger documentation for the country list endpoint.
    """
    return swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="Filter countries by name (case-insensitive, partial match)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'code',
                openapi.IN_QUERY,
                description="Filter countries by code (case-insensitive, partial match)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order results by field (prefix with '-' for descending). Options: name, code, -name, -code",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search across name and code fields",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of results per page (default: 10)",
                type=openapi.TYPE_INTEGER
            ),
        ],
        operation_description="""
        Retrieve a list of countries with filtering, ordering and search capabilities.
        
        Filters:
        - name: Filter by country name (case-insensitive, partial match)
          Example: ?name=united
        
        - code: Filter by country code (case-insensitive, partial match)
          Example: ?code=us
        
        Ordering:
        - name: Order by country name
        - code: Order by country code
        
        Add '-' prefix for descending order, e.g. '-name'
        
        Search:
        - Searches across name and code fields
        
        Pagination:
        - Page size: 10 items per page (default)
        - Use page parameter to navigate pages
        - Use page_size parameter to customize results per page
        """
    )
