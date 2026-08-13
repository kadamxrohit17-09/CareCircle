from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/'), name='root_redirect'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('family.urls')),
    path('api/', include('reports.urls')),
    path('api/', include('reminders.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    # Other APIs will be included here later
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
