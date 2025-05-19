from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from city.views import CityViewSet

# Define common parameters
id_parameter = openapi.Parameter(
    'id', 
    openapi.IN_PATH, 
    description="ID of the city", 
    type=openapi.TYPE_INTEGER
)

# Apply swagger documentation to CityViewSet methods
CityViewSet.list = swagger_auto_schema(
    operation_description="Get a list of all cities",
    operation_summary="List all cities",
    manual_parameters=[
        openapi.Parameter(
            'search', 
            openapi.IN_QUERY, 
            description="Search by city name or country name", 
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'ordering', 
            openapi.IN_QUERY, 
            description="Order by field (e.g. name, country__name, -name for descending)", 
            type=openapi.TYPE_STRING
        )
    ]
)(CityViewSet.list)

CityViewSet.create = swagger_auto_schema(
    operation_description="Create a new city",
    operation_summary="Create city",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'country'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="City name"),
            'country': openapi.Schema(type=openapi.TYPE_INTEGER, description="Country ID")
        }
    )
)(CityViewSet.create)

CityViewSet.retrieve = swagger_auto_schema(
    operation_description="Get details of a specific city",
    operation_summary="Get city details",
    manual_parameters=[id_parameter]
)(CityViewSet.retrieve)

CityViewSet.update = swagger_auto_schema(
    operation_description="Update all fields of a specific city",
    operation_summary="Update city",
    manual_parameters=[id_parameter],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'country'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="City name"),
            'country': openapi.Schema(type=openapi.TYPE_INTEGER, description="Country ID")
        }
    )
)(CityViewSet.update)

CityViewSet.partial_update = swagger_auto_schema(
    operation_description="Update specific fields of a city",
    operation_summary="Partial update city",
    manual_parameters=[id_parameter],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="City name"),
            'country': openapi.Schema(type=openapi.TYPE_INTEGER, description="Country ID")
        }
    )
)(CityViewSet.partial_update)

CityViewSet.destroy = swagger_auto_schema(
    operation_description="Delete a specific city",
    operation_summary="Delete city",
    manual_parameters=[id_parameter]
)(CityViewSet.destroy)
