from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from account.serializers import UserSerializer

from .forms import UserRegisterForm
from .models import Pedido, PedidoSerializer
from .models import Producto, ProductoSerializer
from .models import PedidoProducto, PedidoProductoSerializer
from .models import productoSerializer, productosSerializer
from .sendmail import sender
from django.conf import settings


# mostrar todos los productos
class productos (APIView):
    # metodo GET
    # request: el requisito que pidio el cliente
    # format: es utilizado en el django, para mistrarlo en el test
    def get(self, request, format=None):
        # leer todos los productos de la base de datos
        productos = Producto.objects.all()

        # serializar: convertirlos en josn
        productos = productosSerializer(productos, request)

        # devuelve los producton renrerizados en forma de srting
        return Response(productos.data)


# visualizar un producto
class producto (APIView):
    # metodo GET
    # request: el requisito que pidio el cliente
    # pk: la clave del producto
    # format: es utilizado en el django, para mistrarlo en el test
    def get(self, request, pk, format=None):
        # buscar el producto, que tiene el id iqual al pk
        producto = Producto.objects.get(id=pk)

        # serializar el producto en json
        producto = productoSerializer(producto, request)

        # renderizar el producto json en forma string, para revolverlo al usuario
        return Response(producto.data)


# mostrar todos los pedidos del cliente
class pedidos (generics.RetrieveAPIView):
    # sobre escribir propiedades de la clase, serializacion y autorizacion
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    # metodo GET
    # request: el requisito que pidio el cliente
    # format: es utilizado en el django, para mistrarlo en el test
    def get(self, request, format=None):
        # filtrar los pedidos del cliente
        # order_by -id: ordernar los pedidos del mas reciente al mas antiguo
        pedidos = Pedido.objects.filter(cliente=request.user).order_by("-id")

        # serializar los pedidos en json
        pedidos = PedidoSerializer(pedidos, many=True)

        # renderizar los pedidos json en forma string, para revolverlo al usuario
        return Response(pedidos.data)

# pedidos del cliente


class pedido (generics.RetrieveAPIView):
    # sobre escribir propiedades de la clase, serializacion y autorizacion
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    # visualizar detaller de un pedido
    # request: el requisito que pidio el cliente
    # pk: la clave del producto
    # format: es utilizado en el django, para mistrarlo en el test
    def get(self, request, pk, format=None):
        # filtrar el pedido del cliente, que contenga el pk
        pedido = Pedido.objects.get(id=pk, cliente=request.user)

        # serializar el pedido en json
        pedido = PedidoSerializer(pedido)

        # renderizar el pedido json en forma string, para revolverlo al usuario
        return Response(pedido.data)

    # realizar compra de los productos en la cesta
    # request: el requisito que pidio el cliente
    def post(self, request):
        # buscar los productos que estan en la cesta
        cesta = get_cesta(request)
        if len(cesta) == 0:
            # si no tiene productos, devuelve una notificacion.
            return return_error("No tienes productos en la cesta!")

        # crear un nuevo pedido y añadir el cliente al pedido
        pedido = Pedido()
        pedido.cliente = request.user
        pedido.save()

        # crear el archivo csv y añadir los productos de la cesta
        csv = ['producto,precio,cantidad,total']
        for item in cesta:
            nombre = item.producto.nombre
            precio = item.producto.precio
            cantidad = item.cantidad
            total = precio * cantidad

            item.precio = precio
            item.pedido = pedido
            item.save()

            csv.append(f'{nombre},{precio},{cantidad},{total}')

        # enviar el archibo por email a la empreda
        send_email(pedido, "\n".join(csv))

        # notificar al cliente "Pedido recibido"
        return return_success('Pedido recibido')


# cesta del cliente
class cesta (generics.RetrieveAPIView):
    # sobre escribir propiedades de la clase, serializacion y autorizacion
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    # mostrar todos los productos que estan en la cesta
    # request: es el requisito que pidio el cliente
    # format: es utilizado en el django, para mistrarlo en el test
    def get(self, request, format=None):
        # buscar los productos que estan en la cesta
        cesta = get_cesta(request)

        # serializar la cesta en json
        cesta = PedidoProductoSerializer(cesta, many=True)

        # renderizar la cesta json en forma string, para revolverlo al cliente
        return Response(cesta.data)

    # añadir un nuevo producto a la cesta
    # request: es el requisito que pidio el cliente
    # format: es utilizado en el django, para mistrarlo en el test
    def post(self, request, format=None):
        # leer el producto añadido
        pedido = PedidoProductoSerializer(data=request.data)

        # asegurarse que tenga todos los campos requiridos
        if not pedido.is_valid():
            # si no, notifica al cliente, los campos requiridos
            return return_bad_request(pedido)

        # asegurarse que el producto no esta en la cesta
        producto = pedido.validated_data.get("producto")
        cesta = get_cesta(request).filter(producto=producto)

        # si encuentra el producto en la cesta
        if len(cesta) > 0:
            # notifica al cliente que ya lo añadio
            return return_error('Producto ya esta en cesta!')

        # añade el producto a la cesta del cliente
        pedido.save(cliente=request.user)
        cesta_count = len(get_cesta(request))

        # notifica al cliente los productos que estan en la cesta
        return return_success(f"Producto [{producto}] añadido a la cesta!", cesta_count)

    # modificar la cantidad del producto en la cesta
    # request: es el requisito que pidio el cliente
    # pk: es la clave del producto
    # format: es utilizado en el django, para mistrarlo en el test
    def patch(self, request, pk, format=None):
        # lee la cantidad deseada por el cliente
        cantidad = request.data.get('cantidad')

        # asegura que la cantidad a sido enviada
        if cantidad is None:
            # notifica al cliente que no envio la cantidad
            return return_error('No esta presente la cantidad')

        # asegura que la cantirar es un numero
        if not cantidad.isnumeric():
            # notifica al cliente que debe enviar la cantidad como numero
            return return_error('Cantidad tiene que ser mayor que 1!')

        # asegura que la cantidad es mayor que zero
        if int(cantidad) < 1:
            # notifica al cliente que debe enviar la cantidad mayor que zero
            return return_error('Cantidad tiene que ser mayor que 1!')

        # asegura que el producto esta en la cesta
        pedidos = PedidoProducto.objects.filter(id=pk, cliente=request.user)
        if len(pedidos) == 0:
            # si no, notifica al cliente que no tiene ese pedido en la cesta
            return return_error('No se pudo encontrar el pedido')

        # modificar el pedido y grabarlo
        pedido = pedidos.first()
        pedido.cantidad = cantidad
        pedido.save()

        # notifica al cliente que a sido modificado su pedido
        return return_success(f'cantidad registrada: {cantidad}')

    # borar un producto de la cesta
    # request: es el requisito que pidio el cliente
    # pk: es la clave del producto
    def delete(self, request, pk):
        # buscas el pedido en la cesta
        pedido = PedidoProducto.objects.filter(id=pk, cliente=request.user)
        if len(pedido) == 0:
            # si no esta, notifica al cliente que no tiene ese pedido en la cesta
            return return_error("Producto no en cesta!")

        # guarda el pombre del producto para mostrarlo en la notificacion
        producto = pedido[0].producto

        # bora el pedido de la cesta
        deleted = pedido.delete()

        # notifica al cliente que el producto ya se elimino de la cesta
        return return_success(f'Producto [{producto}] removido de la cesta')


# leer todos los pedidos añadidos a la cesta
# request: es el requisito que pidio el cliente
def get_cesta(request):
    # los productos en la cesta no tienen nubero de pedido, porque aun no an sido comprados
    return PedidoProducto.objects.filter(pedido=None, cliente=request.user)


# renderica el mensage para el cliente, marcado como exitoso
# puedes enviar la cantidad en la cesta, para cuando se modifique la cantidad
def return_success(message, cesta_count=0):
    data = {'success': message}
    if cesta_count > 0:
        # añadir la cantidad de productos en la cesta, para mostrarselo al cliente
        data['cesta_count'] = cesta_count

    # renderiza el mensage
    return Response(data)


# renderica el mensage para el cliente, marcado como abiso
def return_warning(message):
    # renderiza el mensage
    return Response({'warning': message})


# renderica el mensage para el cliente, marcado como informacion
def return_info(message):
    # renderiza el mensage
    return Response({'info': message})


# renderica el mensage para el cliente, marcado como error
def return_error(message):
    # renderiza el mensage
    return Response({'error': message})


# obj: el objeto que tubo el error
# renderica un error de falta de datos para serializar un objeto
def return_bad_request(obj):
    # renderiza el mensage
    return return_error(obj.error)


# enviar un mensage al email de la empresa
def send_email(pedido, productos):
    try:
        sender_email = settings.SENDER_EMAIL
        sender_pass = settings.SENDER_PASS
        reciver_email = settings.RECIVER_EMAIL
        subject_email = settings.SUBJECT_EMAIL

        mail = sender(sender_email, sender_pass)
        mail.attach_content("Productos.csv", productos)
        mail.send(reciver_email, subject_email, f"{pedido}")
    except Exception as e:
        print("ERROR : "+str(e))
