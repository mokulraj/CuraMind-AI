from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [
    # --------------------------------------------------------
    # Django Admin
    # --------------------------------------------------------

    path(
        "admin/",
        admin.site.urls,
    ),

    # --------------------------------------------------------
    # Web UI
    # --------------------------------------------------------

    path(
        "",
        include("web.urls"),
    ),

    # --------------------------------------------------------
    # API Documentation
    # --------------------------------------------------------

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema",
        ),
        name="redoc",
    ),

    # --------------------------------------------------------
    # Main API
    # --------------------------------------------------------

    path(
        "api/v1/",
        include("apps.api.urls"),
    ),

    # --------------------------------------------------------
    # Authentication API
    # --------------------------------------------------------

    path(
        "api/v1/auth/",
        include(
            "apps.users.authentication.urls"
        ),
    ),
]


# ============================================================
# DEVELOPMENT MEDIA FILES
# ============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )


# ============================================================
# STATIC FILES
# ============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )