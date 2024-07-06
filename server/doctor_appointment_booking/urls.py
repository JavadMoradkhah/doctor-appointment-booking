from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('medical/', include('medical.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)