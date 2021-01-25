from rest_framework import serializers


class Pedido (serializers.Serializer):
    name = serializers.CharField(max_length=32)
