from rest_framework import serializers


class Producto(serializers.Serializer):
    name = serializers.CharField(max_length=32)
