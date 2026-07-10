from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots_txt, name="robots"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap"),
    path("yandex_4d153c26552f0309.html", views.yandex_verification, name="yandex_verification"),
    path("errors/400/", views.error_400_preview, name="error_400_preview"),
    path("errors/403/", views.error_403_preview, name="error_403_preview"),
    path("errors/404/", views.error_404_preview, name="error_404_preview"),
    path("errors/500/", views.error_500_preview, name="error_500_preview"),
]
