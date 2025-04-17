from django.urls import path
from . import views

urlpatterns = [
    path('geo-details/', views.GeoDetailsView.as_view(), name='geo-details'),
]
