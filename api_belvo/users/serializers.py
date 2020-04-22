from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """User Serializer."""

    name = serializers.CharField(
        required=True
    )
    email = serializers.EmailField(
        required=True
    )
    age = serializers.IntegerField(
        min_value=0,
        max_value=99
    )

    class Meta:
        """Meta class for User Serializer."""

        model = User
        fields = ('name', 'email', 'age', )
