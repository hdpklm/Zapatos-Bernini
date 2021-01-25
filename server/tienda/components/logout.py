from rest_framework import serializers


class Logout (serializers.Serializer):
    name = serializers.CharField(max_length=32)
