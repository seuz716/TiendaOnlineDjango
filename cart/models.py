from django.db import models
from productos.models import Producto

class Carrito(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'
