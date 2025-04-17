from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.db.models import Q, F
from django.conf import settings
from django.template.loader import render_to_string
from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm
from django.views.decorators.http import require_GET
from django.http import HttpResponseServerError
from django.shortcuts import render, get_object_or_404


# Listar categorías
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'productos/categoria_list.html'
    context_object_name = 'categorias'

# Crear categoría
class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'productos/categoria_form.html'
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

# Listar productos con filtro por categoría y ordenación por precio
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('categoria')

        # Filtro por categoría
        categoria_slug = self.request.GET.get('categoria')
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)

        # Ordenar por precio
        price_filter = self.request.GET.get('priceFilter')
        if price_filter == 'asc':
            queryset = queryset.order_by('precio')
        elif price_filter == 'desc':
            queryset = queryset.order_by('-precio')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Agregamos categorías
        return context

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

# Vista de detalle del producto
class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/producto_detail.html'




@require_GET
def buscar_productos(request):
    categoria_slug = request.GET.get('categoria')
    price_filter = request.GET.get('priceFilter')
    
    # Inicia con todos los productos (puedes agregar select_related para optimizar)
    productos = Producto.objects.all().select_related('categoria')
    
    # Filtro por categoría si se pasó el parámetro
    if categoria_slug:
        productos = productos.filter(categoria__slug=categoria_slug)
    
    # Ordenar según el filtro de precio
    if price_filter == 'asc':
        productos = productos.order_by('precio')
    elif price_filter == 'desc':
        productos = productos.order_by('-precio')
    
    # Renderiza el template parcial con los productos filtrados
    html = render_to_string('productos/_product_grid.html', {'productos': productos})
    return JsonResponse({'html': html})

#

class ProductoClientListView(ListView):
    model = Producto
    template_name = 'productos/producto_client_list.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        # Opcional: Filtra solo productos disponibles y/o agrega ordenación
        queryset = Producto.objects.filter(disponible=True).select_related('categoria')
        # Puedes aplicar filtros de categoría o precio si lo deseas
        categoria_slug = self.request.GET.get('categoria')
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)
        
        price_filter = self.request.GET.get('priceFilter')
        if price_filter == 'asc':
            queryset = queryset.order_by('precio')
        elif price_filter == 'desc':
            queryset = queryset.order_by('-precio')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Para el filtro de categorías en el cliente, si deseas mostrarlas en el navbar
        context['categorias'] = Categoria.objects.all()
        return context    



def filtrar_productos(request):
    try:
        productos = Producto.objects.all()

        # Filtro por búsqueda
        search_query = request.GET.get('search', '').strip()
        if search_query:
            productos = productos.filter(
                Q(nombre__icontains=search_query) | 
                Q(descripcion__icontains=search_query) |
                Q(categoria__nombre__icontains=search_query)
            )

        # Aquí puedes incluir otros filtros (categoría, precio) si los necesitas

        # Renderizamos el grid parcial. Asegúrate de pasar el request para el CSRF token.
        html = render_to_string('productos/_product_grid.html', {'productos': productos}, request=request)
        return JsonResponse({'html': html})
    except Exception as e:
        print(f"❌ Error en filtrar_productos: {e}")
        return HttpResponseServerError("Ocurrió un error al filtrar los productos.")


def filtrar_productos_adm(request):
    categoria_slug = request.GET.get('categoria')
    price_filter = request.GET.get('priceFilter')
    
    # Inicia con todos los productos (puedes agregar select_related para optimizar)
    productos = Producto.objects.all().select_related('categoria')
    
    # Filtro por categoría si se pasó el parámetro
    if categoria_slug:
        productos = productos.filter(categoria__slug=categoria_slug)
    
    # Ordenar según el filtro de precio
    if price_filter == 'asc':
        productos = productos.order_by('precio')
    elif price_filter == 'desc':
        productos = productos.order_by('-precio')
    
    # Renderiza el template parcial con los productos filtrados
    html = render_to_string('productos/_product_gridAdm.html', {'productos': productos})
    return JsonResponse({'html': html})

        