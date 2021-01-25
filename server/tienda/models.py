from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    tamanio = models.IntegerField()
    imagen = models.ImageField(
        default='default.jpg', upload_to='producto_pics')
    desc = models.CharField(max_length=1024, default="")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Pedido #{self.id} del cliente: {self.cliente}'


class PedidoProducto(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, blank=True, null=True, default=None)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        pedido = (self.pedido and f"#{self.pedido.id}") or "[en cesta]"
        return f'Pedido {pedido} del cliente: {self.cliente}, Producto: {self.producto}, Cantidad: {self.cantidad}'


class ProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = '__all__'
        # fields = ('id', 'nombre', 'precio', 'tamanio', 'imagen', 'desc', 'date')

    def get_imagen(self, obj):
        request = self.context.get('request')
        photo_url = obj.imagen.url
        return request.build_absolute_uri(photo_url)


class PedidoSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = '__all__'
        # fields = ('id', 'nombre', 'precio', 'tamanio', 'imagen', 'desc', 'date')

    def get_productos(self, obj):
        result = []
        productos = obj.pedidoproducto_set.all()
        for item in productos:
            producto = PedidoProductoSerializer(item)
            result.append(producto.data)
        return result


class PedidoProductoSerializer(serializers.ModelSerializer):
    producto_id = serializers.SerializerMethodField()
    nombre = serializers.SerializerMethodField()
    tamanio = serializers.SerializerMethodField()
    precio = serializers.SerializerMethodField()
    imagen = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = PedidoProducto
        fields = '__all__'
        # fields = ('id', 'nombre', 'precio', 'tamanio', 'imagen', 'desc', 'date')

    def get_producto_id(self, obj):
        return obj.producto.id

    def get_nombre(self, obj):
        return obj.producto.nombre

    def get_tamanio(self, obj):
        return obj.producto.tamanio

    def get_precio(self, obj):
        return obj.precio or obj.producto.precio

    def get_imagen(self, obj):
        return obj.producto.imagen.url

    def get_total(self, obj):
        return (obj.precio or obj.producto.precio) * obj.cantidad

    def get_cliente(self, obj):
        return obj.cliente


def productoSerializer(producto, request):
    return ProductoSerializer(producto, context={"request": request})


def productosSerializer(productos, request):
    return ProductoSerializer(productos, many=True, context={"request": request})
