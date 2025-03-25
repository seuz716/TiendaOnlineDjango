from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'icono')  # Muestra estos campos en la lista
    search_fields = ('nombre',)  # Permite buscar por nombre
    prepopulated_fields = {'slug': ('nombre',)}  # Genera automáticamente el slug desde el nombre
    ordering = ('nombre',)  # Ordena por nombre
    list_per_page = 20  # Limita el número de elementos por página

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'disponible', 'categoria', 'creado')  # Campos visibles en la lista
    search_fields = ('nombre', 'categoria__nombre')  # Búsqueda por nombre y categoría
    list_filter = ('disponible', 'categoria')  # Filtrado por disponibilidad y categoría
    prepopulated_fields = {'slug': ('nombre',)}  # Genera automáticamente el slug desde el nombre
    readonly_fields = ('creado', 'actualizado')  # Solo lectura para fechas automáticas
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'slug', 'descripcion', 'categoria', 'imagen')
        }),
        ('Precio y disponibilidad', {
            'fields': ('precio', 'stock', 'disponible')
        }),
        ('Datos avanzados', {
            'fields': ('caracteristicas',),
            'classes': ('collapse',)  # Oculta esta sección por defecto
        }),
        ('Fechas', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-creado',)  # Ordena por fecha de creación descendente
    list_editable = ('precio', 'stock', 'disponible')  # Permite edición directa desde la lista
    list_per_page = 20  # Limita los productos por página
