from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# rename admin dashboard
admin.site.site_header = "Garage  Portal"
admin.site.site_title = "Garage Partners"
admin.site.index_title = "Welcome to Garage  Management Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('denso-hq/', include('apps.backoffice.urls')),
    path('workshop/', include('apps.workshop.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
