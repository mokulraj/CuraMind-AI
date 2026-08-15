from django.urls import path

from .web_views import dashboard_home


app_name = "dashboard_web"


urlpatterns = [
    path(
        "",
        dashboard_home,
        name="home",
    ),
]