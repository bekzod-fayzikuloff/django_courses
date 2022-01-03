"""online_coursres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework import permissions
from rest_framework.schemas import get_schema_view as default_schema_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

api_urls = [path("auth/", include("user.urls")), path("", include("courses.urls"))]

schema_view = get_schema_view(
    openapi.Info(
        title="Courses API",
        default_version="v1",
        description="Courses API documentation endpoints",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
    path(
        "docs/",
        TemplateView.as_view(template_name="swagger-ui.html", extra_context={"schema_url": "openapi-schema"}),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        TemplateView.as_view(template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}),
        name="redoc",
    ),
    path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger-yasg/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-yasg"),
    path("redoc-yasg/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-yasg"),
    path(
        "openapi",
        default_schema_view(title="Your Project", description="API for all things …", version="1.0.0"),
        name="openapi-schema",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
