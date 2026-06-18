from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico", permanent=True)),
    path('', include('catalog.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = "catalog.views.bad_request"
handler403 = "catalog.views.permission_denied"
handler404 = "catalog.views.page_not_found"
handler500 = "catalog.views.server_error"
