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


# OK
class productos (APIView):
    def get(self, request, format=None):
        productos = Producto.objects.all()
        productos = productosSerializer(productos, request)
        return Response(productos.data)


# OK
class producto (APIView):
    def get(self, request, pk, format=None):
        producto = Producto.objects.get(id=pk)
        producto = productoSerializer(producto, request)
        return Response(producto.data)


# OK
class pedidos (generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, format=None):
        pedidos = Pedido.objects.filter(cliente=request.user).order_by("-id")
        pedidos = PedidoSerializer(pedidos, many=True)
        #print('pedidos:', pedidos.productos)
        return Response(pedidos.data)


# OK
class pedido (generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk, format=None):
        pedido = Pedido.objects.get(id=pk, cliente=request.user)
        pedido = PedidoSerializer(pedido)
        return Response(pedido.data)

    def post(self, request):
        cesta = get_cesta(request)
        if len(cesta) == 0:
            return return_error("No tienes productos en la cesta!")

        pedido = Pedido()
        pedido.cliente = request.user
        pedido.save()

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

        send_email(pedido, "\n".join(csv))
        return return_success('Pedido recibido')


# OK
class cesta (generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, format=None):
        cesta = get_cesta(request)
        cesta = PedidoProductoSerializer(cesta, many=True)
        return Response(cesta.data)

    def post(self, request, format=None):
        print("user", request.user)
        pedido = PedidoProductoSerializer(data=request.data)
        if not pedido.is_valid():
            return return_bad_request(pedido)

        producto = pedido.validated_data.get("producto")
        cesta = get_cesta(request).filter(producto=producto)
        if len(cesta) > 0:
            return return_error('Producto ya esta en cesta!')

        pedido.save(cliente=request.user)
        cesta_count = len(get_cesta(request))
        return return_success(f"Producto [{producto}] añadido a la cesta!", cesta_count)

    def patch(self, request, pk, format=None):
        cantidad = request.data.get('cantidad')
        if cantidad is None:
            return return_error('No esta presente la cantidad')

        if not cantidad.isnumeric():
            return return_error('Cantidad tiene que ser mayor que 1!')

        if int(cantidad) < 1:
            return return_error('Cantidad tiene que ser mayor que 1!')

        pedidos = PedidoProducto.objects.filter(id=pk, cliente=request.user)
        if len(pedidos) == 0:
            return return_error('No se pudo encontrar el pedido')

        pedido = pedidos.first()
        pedido.cantidad = cantidad
        pedido.save()

        return return_success(f'cantidad registrada: {cantidad}')

    def delete(self, request, pk):
        pedido = PedidoProducto.objects.filter(id=pk, cliente=request.user)
        if len(pedido) == 0:
            return return_error("Producto no en cesta!")

        producto = pedido[0].producto
        deleted = pedido.delete()
        return return_success(f'Producto [{producto}] removido de la cesta')


def get_cesta(request):
    return PedidoProducto.objects.filter(pedido=None, cliente=request.user)


def return_success(message, cesta_count=0):
    data = {'success': message}
    if cesta_count > 0:
        data['cesta_count'] = cesta_count
    return Response(data)


def return_warning(message):
    return Response({'warning': message})


def return_info(message):
    return Response({'info': message})


def return_error(message):
    return Response({'error': message})


def return_bad_request(obj):
    return return_error(obj.error)


def register_old(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'tienda/register.html', {'form': form})


def send_email(pedido, productos):
    mail = sender("inibir.test.123@gmail.com", "cuentatest123")
    mail.attach_content("Productos.csv", productos)
    mail.send("hdaoud10@gmail.com",
              f"{pedido}",
              f"{pedido}")
