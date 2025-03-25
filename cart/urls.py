from django.urls import path
from .views import (
    CartListView, 
    CartDetailView, 
    CartCreateView, 
    CartUpdateView, 
    CartDeleteView, 
    enviar_whatsapp
)

urlpatterns = [
    path('', CartListView.as_view(), name='cart-list'),              # Listar ítems
    path('<int:pk>/', CartDetailView.as_view(), name='cart-detail'), # Detalle de un ítem
    path('add/', CartCreateView.as_view(), name='cart-add'),         # Añadir ítem
    path('<int:pk>/edit/', CartUpdateView.as_view(), name='cart-edit'), # Editar ítem
    path('<int:pk>/delete/', CartDeleteView.as_view(), name='cart-delete'), # Eliminar ítem
    path('whatsapp/', enviar_whatsapp, name='cart-whatsapp'),        # Enviar a WhatsApp
]
