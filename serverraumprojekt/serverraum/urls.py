from django.contrib import admin
from django.urls import path
from .views import startseite, sensordaten_api, tuerstatus_api


urlpatterns = [
    path("", startseite),
    path("admin/", admin.site.urls),
    path("api/sensordaten/", sensordaten_api),
    path("api/tuerstatus/", tuerstatus_api),
]