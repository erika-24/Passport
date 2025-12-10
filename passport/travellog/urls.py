from django.contrib import admin
from django.urls import path

from .views import home, export_to_xlsx

urlpatterns = [
    path('', home),
    path("export/xlsx/", export_to_xlsx, name="export_to_xlsx"),
]