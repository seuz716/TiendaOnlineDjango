# views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm
from django.http import JsonResponse
from django.db.models import Q

# Listar categorías
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'products/categoria_list.html'
    context_object_name = 'categorias'

# Crear categoría
class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'products/categoria_form.html'
    success_url = reverse_lazy('categoria-list')

# Editar categoría
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'productos/categoria_form.html'
    success_url = reverse_lazy('categoria-list')

# Eliminar categoría
class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'productos/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria-list')
# Listar productos
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

# Crear producto
class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto-list')

# Editar producto
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto-list')

# Eliminar producto
class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto-list')



def buscar_productos(request):
    query = request.GET.get('search', '')
    productos = Producto.objects.filter(
        Q(nombre__icontains=query) | 
        Q(descripcion__icontains=query)
    ).values('nombre', 'precio', 'imagen')
    
    return JsonResponse({
        'results': list(productos)
    })