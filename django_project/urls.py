from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from nuts.api import api

urlpatterns = [
    path("api/v1.0/", api.urls),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
