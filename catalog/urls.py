from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("favorites/", views.favorite_products, name="favorite_products"),
    path("favorites/<int:pk>/toggle/", views.toggle_favorite_product, name="toggle_favorite_product"),
    path("prices/", views.price_upload_registry, name="price_upload_registry"),
    path("prices/<int:pk>/confirm/", views.price_upload_confirm, name="price_upload_confirm"),
    path("prices/<int:pk>/download/", views.price_upload_download, name="price_upload_download"),
    path("prices/export/database/", views.export_database_excel, name="export_database_excel"),
]
