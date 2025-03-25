from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Carrito
from productos.models import Producto

# ✅ LISTAR TODOS LOS ITEMS DEL CARRITO
class CartListView(ListView):
    model = Carrito
    template_name = 'cart/cart_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.create()
        return Carrito.objects.filter(session_key=session_key)

# ✅ DETALLE DE UN ITEM DEL CARRITO
class CartDetailView(DetailView):
    model = Carrito
    template_name = 'cart/cart_detail.html'
    context_object_name = 'item'

# ✅ CREAR UN ITEM EN EL CARRITO
class CartCreateView(CreateView):
    model = Carrito
    template_name = 'cart/cart_form.html'
    fields = ['producto', 'cantidad']

    def form_valid(self, form):
        # Asignar la sesión actual al carrito
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.create()
        form.instance.session_key = self.request.session.session_key
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cart-list')

# ✅ ACTUALIZAR UN ITEM EN EL CARRITO
class CartUpdateView(UpdateView):
    model = Carrito
    template_name = 'cart/cart_form.html'
    fields = ['cantidad']

    def get_success_url(self):
        return reverse_lazy('cart-list')

# ✅ ELIMINAR UN ITEM DEL CARRITO
class CartDeleteView(DeleteView):
    model = Carrito
    template_name = 'cart/cart_confirm_delete.html'
    success_url = reverse_lazy('cart-list')
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils.http import urlencode
from .models import Carrito

def enviar_whatsapp(request):
    carrito = Carrito.objects.all()
    mensaje = "\n".join([f"{item.producto.nombre} - {item.cantidad}" for item in carrito])
    params = urlencode({"text": mensaje})
    url = f"https://api.whatsapp.com/send?phone=+573001234567&{params}"
    return redirect(url)
