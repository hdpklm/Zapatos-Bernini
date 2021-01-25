from django.urls import path
from .views import producto, productos, pedidos, pedido, cesta

urlpatterns = [
    path('productos/', productos.as_view()),
    path('producto/<int:pk>', producto.as_view()),
    path('pedidos/', pedidos.as_view()),
    path('pedido/', pedido.as_view()),
    path('cesta/', cesta.as_view()),
    path('cesta/<int:pk>', cesta.as_view()),
]
