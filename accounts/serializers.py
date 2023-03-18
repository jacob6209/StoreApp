from djoser.serializers import UserCreateSerializer


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["id","email","username","password"]
