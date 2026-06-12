from django.contrib import admin
from django.urls import path
from .views import startseite, sensordaten_api


urlpatterns = [
    path("", startseite),
    path("admin/", admin.site.urls),
    path("api/sensordaten/", sensordaten_api),
]