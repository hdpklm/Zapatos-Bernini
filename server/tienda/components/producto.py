from rest_framework import serializers


class test_serialize(serializers.Serializer):
    name = serializers.CharField(max_length=32)
