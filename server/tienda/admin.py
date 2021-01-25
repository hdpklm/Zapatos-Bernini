from django.contrib import admin
from .models import Pedido, Producto, PedidoProducto

admin.site.register(Producto)
admin.site.register(PedidoProducto)
admin.site.register(Pedido)
