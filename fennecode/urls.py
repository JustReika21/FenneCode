from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from core.views import custom_handler403, custom_handler404, custom_handler500

handler403 = custom_handler403
handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('accounts.urls')),
    path('profile/', include('user_profile.urls')),
    path('courses/', include('courses.urls')),
    path('api/', include('api.urls')),
    path('', include('about.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
