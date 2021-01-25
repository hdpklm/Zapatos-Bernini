from rest_framework import serializers


class Register (serializers.Serializer):
    username = serializers.CharField(
        max_length=32, read_only=True, required=True)

    password1 = serializers.CharField(
        max_length=32, read_only=True, required=True)

    password2 = serializers.CharField(
        max_length=32, read_only=True, required=True)

    fullname = serializers.CharField(
        max_length=64, read_only=True, required=True)

    email = serializers.CharField(
        max_length=962, read_only=True, required=True)
