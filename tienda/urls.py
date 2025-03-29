from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Importación faltante
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', RedirectView.as_view(url='/accounts/login/')),  # Redirección
    path('accounts/', include('django.contrib.auth.urls')),  # URLs de autenticación
    path('', include('productos.urls')),
    path('cart/', include('cart.urls')),
]

# Handlers de errores
handler404 = 'tienda.views.custom_404'
handler500 = 'tienda.views.custom_500'

# Configuración para desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path('404/', views.custom_404),
        path('500/', views.custom_500),
    ]