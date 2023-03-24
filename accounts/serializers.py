from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["id","email","username","password"]

