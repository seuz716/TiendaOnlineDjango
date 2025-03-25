from django.urls import path
from .views import (
    CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView,
    ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
)

urlpatterns = [
    # Categorías
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/nueva/', CategoriaCreateView.as_view(), name='categoria-create'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categorias/eliminar/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria-delete'),

    # Productos
    path('', ProductoListView.as_view(), name='producto-list'),
    path('productos/nuevo/', ProductoCreateView.as_view(), name='producto-create'),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto-update'),
    path('productos/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto-delete'),
]
