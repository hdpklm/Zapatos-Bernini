from rest_framework import serializers


class Cesta (serializers.Serializer):
    name = serializers.CharField(max_length=32)
