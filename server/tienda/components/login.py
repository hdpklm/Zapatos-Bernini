from rest_framework import serializers


class Login (serializers.Serializer):
    username = serializers.CharField(
        max_length=32, read_only=True, required=True)
    password = serializers.CharField(
        max_length=32, read_only=True, required=True)
